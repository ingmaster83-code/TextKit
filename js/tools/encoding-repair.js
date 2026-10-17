TK.tool('encoding-repair', {
  inputs: [{ id: 'in', label: ['깨진 텍스트 (한 줄에 하나씩 넣어도 됩니다)', 'Garbled text (one sample per line is fine)'], rows: 6, sample: 'ì•ˆë…•í•˜ì„¸ìš”\nÃ©tÃ© cafÃ©\n¾È³çÇÏ¼¼¿ä\nâ€œSmart quotesâ€\n%EC%95%88%EB%85%95\n&#xC548;&#xB155;\n\\uC548\\uB155' }],
  options: [
    { id: 'all', type: 'checkbox', label: ['점수가 낮은 후보도 모두 표시', 'Show low-scoring candidates too'], default: false },
    { id: 'encs', type: 'select', label: ['시도할 문자 집합', 'Character sets to try'], choices: [['ko', ['한국어 위주 (UTF-8, EUC-KR/CP949, CP1252)', 'Korean focus (UTF-8, EUC-KR / CP949, CP1252)']], ['cjk', ['한·중·일 (EUC-KR, Shift_JIS, GBK, Big5, EUC-JP)', 'CJK (EUC-KR, Shift_JIS, GBK, Big5, EUC-JP)']], ['all', ['전부 + 키릴(CP1251)', 'All + Cyrillic (CP1251)']]], default: 'ko' }
  ],
  outputs: [{ id: 'best', label: ['가장 그럴듯한 복구 결과', 'Best repair'], kind: 'code', ext: 'txt' }, { id: 'table', label: ['후보', 'Candidates'], kind: 'table' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var input = String(v['in'] == null ? '' : v['in']); if (!input.trim()) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    if (typeof TextDecoder === 'undefined') throw new Error(t('이 브라우저는 TextDecoder 를 지원하지 않습니다', 'This browser does not support TextDecoder'));
    var lines = input.split(/\r?\n/).filter(function (l) { return l.trim() !== ''; }).slice(0, 50);
    var encList = o.encs === 'ko' ? ['euc-kr'] : o.encs === 'cjk' ? ['euc-kr', 'shift_jis', 'gbk', 'big5', 'euc-jp'] : ['euc-kr', 'shift_jis', 'gbk', 'big5', 'euc-jp', 'windows-1251'];
    var maps = {};
    function dec(enc, bytes, fatal) { return new TextDecoder(enc, { fatal: !!fatal }).decode(new Uint8Array(bytes)); }
    function reverseMap(enc) {
      if (maps[enc]) return maps[enc];
      var m = new Map(), i, j, s;
      for (i = 0; i < 256; i++) { try { s = dec(enc, [i]); } catch (e) { continue; } if (s.length === 1 && s !== '�' && !m.has(s)) m.set(s, [i]); }
      if (/euc|shift|gbk|big5|949/.test(enc)) {
        for (i = 0x81; i <= 0xFE; i++) for (j = 0x40; j <= 0xFE; j++) { try { s = dec(enc, [i, j]); } catch (e) { continue; } if (s.length >= 1 && s.indexOf('�') < 0 && Array.from(s).length === 1 && !m.has(s)) m.set(s, [i, j]); }
      }
      maps[enc] = m; return m;
    }
    function toBytes(text, enc) {
      var m = reverseMap(enc), out = [];
      for (var ch of text) { var b = m.get(ch); if (!b) return null; for (var k = 0; k < b.length; k++) out.push(b[k]); }
      return out;
    }
    var lossy = false;
    function utf8(bytes) { try { return dec('utf-8', bytes, true); } catch (e) { return null; } }
    function utf8Loose(bytes) { var s = utf8(bytes); if (s !== null) return s; var r = dec('utf-8', bytes, false), bad = (r.match(/�/g) || []).length; return bad && bad <= Math.max(1, Math.floor(r.length * 0.15)) ? r : null; }
    /* 모지바케(글자 깨짐)가 만드는 대표적인 이중 문자 패턴 */
    var SIGN = /Ã[\u0080-¿]|Â[ -¿]|â€|ì[•\u0080-¿‘-›]|ë[…\u0080-¿‘-›]|í[•\u0080-¿]|ê[°\u0080-¿]|ï¿½|Ð[\u0080-¿]|Ñ[\u0080-¿]/g;
    function score(s) {
      var cps = Array.from(s); if (!cps.length) return 0;
      var letters = 0, odd = 0, ctrl = 0, fffd = 0, mixedWords = 0, words = 0;
      cps.forEach(function (c) { if (c === '�') fffd++; else if (/[\p{L}\p{N}\p{Z}\p{P}\p{S}]/u.test(c)) { if (/\p{L}/u.test(c)) letters++; } else odd++; if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/.test(c)) ctrl++; });
      s.split(/\s+/).forEach(function (w) { if (/\p{L}/u.test(w)) { words++; if (/[A-Za-z]/.test(w) && /[ㄱ-ㆎ가-힣぀-ヿ一-鿿]/.test(w)) mixedWords++; } });
      var sig = (s.match(SIGN) || []).length;
      var sc = 1 - 0.8 * (odd / cps.length) - 0.7 * (ctrl / cps.length) - 0.6 * (fffd / cps.length) - Math.min(0.6, 0.35 * sig * 2 / Math.max(2, cps.length / 2)) - (words ? 0.5 * (mixedWords / words) : 0);
      var l1 = 0; cps.forEach(function (c) { if (/[¡-¿À-ÿ]/.test(c)) l1++; });
      sc -= 0.6 * Math.max(0, l1 / cps.length - 0.25);
      if (!letters) sc -= 0.3;
      return Math.max(0, Math.min(1, sc));
    }
    var rows = [], bestAll = [], notes = [], anyFix = 0;
    function addCand(list, method, res, orig) { if (res !== null && res !== undefined && res !== orig) list.push({ method: method, text: res, score: score(res) }); }
    lines.forEach(function (line, li) {
      var cands = [], baseScore = score(line);
      /* A. UTF-8 바이트를 CP1252(Latin-1) 로 잘못 해석 */
      var b1252 = toBytes(line, 'windows-1252'), a = b1252 && utf8Loose(b1252); addCand(cands, t('UTF-8 을 Latin-1(CP1252)로 잘못 읽음', 'UTF-8 misread as Latin-1 (CP1252)'), a, line);
      if (a) { var b2 = toBytes(a, 'windows-1252'), a2 = b2 && utf8Loose(b2); addCand(cands, t('위 과정이 두 번 일어남 (이중 인코딩)', 'Double-encoded (the above twice)'), a2, line); }
      encList.forEach(function (enc) {
        /* B. UTF-8 바이트를 enc 로 잘못 해석 */
        var bb = toBytes(line, enc); addCand(cands, t('UTF-8 을 ' + enc + ' 로 잘못 읽음', 'UTF-8 misread as ' + enc), bb && utf8(bb), line);
        /* C. enc 바이트를 CP1252 로 잘못 해석 */
        if (b1252) { try { addCand(cands, t(enc + ' 를 Latin-1(CP1252)로 잘못 읽음', enc + ' misread as Latin-1 (CP1252)'), dec(enc, b1252, true), line); } catch (e) { } }
      });
      /* D. 이스케이프 표기 */
      if (/%[0-9A-Fa-f]{2}/.test(line)) { try { addCand(cands, t('퍼센트 인코딩(URL)', 'Percent-encoding (URL)'), decodeURIComponent(line.replace(/\+/g, ' ')), line); } catch (e) { var pb = []; line.replace(/%([0-9A-Fa-f]{2})/g, function (m, h) { pb.push(parseInt(h, 16)); return m; }); } }
      if (/&#x?[0-9A-Fa-f]+;|&[a-z]+;/i.test(line)) addCand(cands, t('HTML 엔티티', 'HTML entities'), line.replace(/&#x([0-9A-Fa-f]+);/g, function (m, h) { return String.fromCodePoint(parseInt(h, 16)); }).replace(/&#(\d+);/g, function (m, d) { return String.fromCodePoint(+d); }).replace(/&(amp|lt|gt|quot|apos|nbsp);/g, function (m, n) { return { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' }[n]; }), line);
      if (/\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|\\x[0-9A-Fa-f]{2}/.test(line)) addCand(cands, t('\\uXXXX 이스케이프', '\\uXXXX escapes'), line.replace(/\\u\{([0-9A-Fa-f]+)\}|\\u([0-9A-Fa-f]{4})|\\U([0-9A-Fa-f]{8})|\\x([0-9A-Fa-f]{2})/g, function (m, a1, a2, a3, a4) { return String.fromCodePoint(parseInt(a1 || a2 || a3 || a4, 16)); }), line);
      if (/=\?[^?]+\?[BbQq]\?[^?]*\?=/.test(line)) addCand(cands, t('MIME 인코딩 단어 (=?UTF-8?B?…?=)', 'MIME encoded-words (=?UTF-8?B?...?=)'), line.replace(/=\?([^?]+)\?([BbQq])\?([^?]*)\?=/g, function (m, cs, enc, body) { try { var bytes; if (/b/i.test(enc)) { var bs = atob(body), u = []; for (var i = 0; i < bs.length; i++) u.push(bs.charCodeAt(i)); bytes = u; } else { bytes = []; body.replace(/_/g, ' ').replace(/=([0-9A-Fa-f]{2})|(.)/g, function (mm, h, c) { if (h) bytes.push(parseInt(h, 16)); else bytes.push(c.charCodeAt(0)); return mm; }); } return dec(cs, bytes); } catch (e) { return m; } }), line);
      if (/(?:=[0-9A-F]{2}){3,}/.test(line)) { var qb = []; line.replace(/=([0-9A-F]{2})|(.)/gs, function (m, h, c) { if (h) qb.push(parseInt(h, 16)); else qb.push(c.charCodeAt(0)); return m; }); addCand(cands, t('Quoted-Printable', 'Quoted-Printable'), utf8(qb), line); }
      /* 정렬: 점수 높은 순, 같으면 더 짧은 쪽 */
      cands.sort(function (x, y) { return y.score - x.score || x.text.length - y.text.length; });
      var shown = cands.filter(function (c) { return o.all || c.score >= Math.min(0.7, baseScore + 0.15); });
      shown.slice(0, 6).forEach(function (c) { rows.push([String(li + 1), line.length > 28 ? line.slice(0, 28) + '…' : line, c.method, c.text.length > 60 ? c.text.slice(0, 60) + '…' : c.text, Math.round(c.score * 100) + '%']); });
      var best = shown[0];
      if (best && (best.score > baseScore + 0.05 || /퍼센트|Percent|HTML|이스케이프|escapes|MIME|Quoted/.test(best.method))) { bestAll.push(best.text); anyFix++; } else bestAll.push(line);
      if (!shown.length) rows.push([String(li + 1), line.length > 28 ? line.slice(0, 28) + '…' : line, t('(복구 후보 없음)', '(no repair candidate)'), '—', Math.round(baseScore * 100) + '%']);
    });
    if (!anyFix) notes.push('⚠️ ' + t('복구 가능한 후보를 찾지 못했습니다. 이미 정상 텍스트이거나, 바이트가 대체 문자(�)로 사라진 손실 상태일 수 있습니다 — 손실된 글자는 복구할 수 없으니 원본 파일을 다시 열 때 올바른 인코딩을 선택하세요', 'No repair candidate found. The text may already be fine or the bytes may have been lost to replacement characters (�), which cannot be recovered; reopen the original with the correct encoding'));
    if (/�/.test(input)) notes.push('ℹ️ ' + t('대체 문자(�)가 포함되어 있습니다. 이 글자는 원래 바이트 정보가 사라진 것이라 복구되지 않습니다', 'Replacement characters (�) are present; their original bytes are gone and cannot be restored'));
    notes.push('ℹ️ ' + t('복구는 "잘못 해석한 규칙을 거꾸로 적용"하는 방식이라 점수(그럴듯함)가 높은 후보를 사람이 확인해야 합니다. 일부 글자가 손실된 문서는 완전 복구되지 않을 수 있습니다', 'Repair works by reversing a wrong decoding, so a person should check the highest-scoring candidate; documents that lost some bytes may not be fully recoverable'));
    notes.push('ℹ️ ' + t('흔한 증상: "ì•ˆë…•" (UTF-8 을 Latin-1 로), "Ã©" (é 의 UTF-8), "â€™" (’ 의 UTF-8), "¾È³ç" (EUC-KR 을 Latin-1 로), "�ȳ�" (UTF-8 한글을 EUC-KR 로 읽다 손실)', 'Common signs: "ì•ˆë…•" (UTF-8 read as Latin-1), "Ã©" (UTF-8 for é), "â€™" (UTF-8 for ’), "¾È³ç" (EUC-KR read as Latin-1)'));
    return { _status: anyFix ? t('✅ ' + anyFix + '/' + lines.length + '줄을 복구했습니다', '✅ Repaired ' + anyFix + ' of ' + lines.length + ' line(s)') : { ok: 'info', msg: t('복구 후보 없음', 'No repair candidates') }, best: bestAll.join('\n'), table: { head: [['줄', 'Line'], ['원본', 'Original'], ['복구 방식', 'Method'], ['결과', 'Result'], ['그럴듯함', 'Plausibility']], rows: rows }, issues: notes };
  }
});
