TK.tool('line-ending-converter', {
  inputs: [
    { id: 'in', label: ['텍스트 (붙여 넣은 텍스트는 브라우저가 줄바꿈을 LF 로 통일합니다 — 정확한 분석은 파일 선택)', 'Text (the browser normalises pasted text to LF; choose a file for an accurate analysis)'], rows: 8, sample: 'first line\\r\\nsecond line\\nthird line\\rfourth line\\r\\n', show: function (o) { return o.mode !== 'file'; } },
    { id: 'file', type: 'file', label: ['텍스트 파일 선택 (서버로 전송되지 않습니다)', 'Choose a text file (never uploaded)'], show: function (o) { return o.mode === 'file'; } }
  ],
  sampleOptions: { unesc: true },
  options: [
    { id: 'mode', type: 'select', label: ['입력 방식', 'Input'], choices: [['text', ['텍스트 붙여 넣기', 'Paste text']], ['file', ['파일 선택', 'Choose a file']]], default: 'text' },
    { id: 'to', type: 'select', label: ['변환할 줄바꿈', 'Convert to'], choices: [['lf', 'LF (\\n) — Linux · macOS'], ['crlf', 'CRLF (\\r\\n) — Windows'], ['cr', 'CR (\\r) — Classic Mac'], ['keep', ['변환하지 않고 분석만', 'Analyse only']]], default: 'lf' },
    { id: 'final', type: 'select', label: ['마지막 줄바꿈', 'Final newline'], choices: [['keep', ['그대로', 'Keep as is']], ['add', ['없으면 추가', 'Add if missing']], ['remove', ['제거', 'Remove']]], default: 'keep' },
    { id: 'unesc', type: 'checkbox', label: ['입력의 \\r \\n 표기를 실제 줄바꿈으로 해석 (붙여 넣기 예시용)', 'Treat \\r and \\n in the input as real line breaks (for pasted examples)'], default: false, show: function (o) { return o.mode !== 'file'; } },
    { id: 'trim', type: 'checkbox', label: ['줄 끝 공백 제거', 'Trim trailing whitespace'], default: false },
    { id: 'bom', type: 'select', label: ['BOM', 'BOM'], choices: [['keep', ['그대로', 'Keep']], ['remove', ['제거', 'Remove']], ['add', ['추가', 'Add']]], default: 'keep' }
  ],
  outputs: [{ id: 'info', label: ['분석', 'Analysis'], kind: 'kv' }, { id: 'lines', label: ['혼용된 줄바꿈 (처음 50개)', 'Mixed line breaks (first 50)'], kind: 'table' }, { id: 'out', label: ['변환 결과', 'Result'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var text, name = '';
    if (o.mode === 'file') { var f = v.file; if (!f || f.text == null) throw new Error(t('파일을 선택하세요', 'Choose a file')); text = f.text; name = f.name; }
    else {
      text = String(v['in'] == null ? '' : v['in']);
      if (!text.length) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
      if (o.unesc) text = text.replace(/\\r\\n|\\r|\\n/g, function (m) { return m === '\\r\\n' ? '\r\n' : m === '\\r' ? '\r' : '\n'; });
    }
    var hadBom = text.charCodeAt(0) === 0xFEFF;
    var body = hadBom ? text.slice(1) : text;
    var crlf = 0, lf = 0, cr = 0, rows = [], i = 0, n = body.length, kinds = [];
    while (i < n) {
      var c = body[i];
      if (c === '\r') { if (body[i + 1] === '\n') { crlf++; kinds.push('CRLF'); i += 2; } else { cr++; kinds.push('CR'); i++; } }
      else if (c === '\n') { lf++; kinds.push('LF'); i++; }
      else i++;
    }
    var total = crlf + lf + cr, used = (crlf ? 1 : 0) + (lf ? 1 : 0) + (cr ? 1 : 0), mixed = used > 1;
    var dom = crlf >= lf && crlf >= cr ? 'CRLF' : lf >= cr ? 'LF' : 'CR';
    if (mixed) { for (var k = 0; k < kinds.length && rows.length < 50; k++) if (kinds[k] !== dom) rows.push([String(k + 1), kinds[k], dom]); }
    var lastKind = kinds.length ? kinds[kinds.length - 1] : '';
    var endsWithNl = /[\r\n]$/.test(body);
    var trailingWs = (body.match(/[ \t]+(?=\r\n|\n|\r|$)/g) || []).length;
    var target = o.to === 'crlf' ? '\r\n' : o.to === 'cr' ? '\r' : o.to === 'lf' ? '\n' : null;
    var out = body;
    if (o.trim) out = out.replace(/[ \t]+(?=\r\n|\n|\r|$)/g, '');
    if (target !== null) out = out.replace(/\r\n|\r|\n/g, target);
    var nl = target !== null ? target : (dom === 'CRLF' ? '\r\n' : dom === 'CR' ? '\r' : '\n');
    if (o.final === 'add' && !/[\r\n]$/.test(out) && out.length) out += nl;
    else if (o.final === 'remove') out = out.replace(/(\r\n|\r|\n)+$/, '');
    var bomOut = o.bom === 'add' ? true : o.bom === 'remove' ? false : hadBom;
    if (bomOut) out = '﻿' + out;
    var bytes = function (s) { return new TextEncoder().encode(s).length; };
    var info = [[['파일', 'File'], name || t('(붙여 넣은 텍스트)', '(pasted text)')], [['LF (\\n)', 'LF (\\n)'], String(lf)], [['CRLF (\\r\\n)', 'CRLF (\\r\\n)'], String(crlf)], [['CR (\\r)', 'CR (\\r)'], String(cr)], [['줄 수', 'Lines'], String(total + (endsWithNl || !body.length ? 0 : 1))], [['주된 줄바꿈', 'Dominant ending'], total ? dom : t('없음', 'none')], [['혼용 여부', 'Mixed endings'], mixed ? t('예 — 서로 다른 줄바꿈이 섞여 있습니다', 'Yes - different endings are mixed') : t('아니오', 'No')], [['마지막 줄바꿈', 'Final newline'], endsWithNl ? t('있음 (' + lastKind + ')', 'yes (' + lastKind + ')') : t('없음', 'none')], [['BOM', 'BOM'], hadBom ? 'UTF-8 BOM (EF BB BF)' : t('없음', 'none')], [['줄 끝 공백이 있는 곳', 'Trailing whitespace spots'], String(trailingWs)], [['크기', 'Size'], bytes(text) + ' B → ' + bytes(out) + ' B']];
    var notes = [];
    if (o.mode !== 'file' && !o.unesc) notes.push('ℹ️ ' + t('붙여 넣은 텍스트는 브라우저가 줄바꿈을 LF 로 통일해 CRLF·CR 을 구분할 수 없습니다. 실제 줄바꿈을 분석하려면 파일을 선택하세요', 'Browsers normalise pasted text to LF, so CRLF and CR cannot be told apart. Choose a file to analyse the real line breaks'));
    if (mixed) notes.push('⚠️ ' + t('줄바꿈이 섞여 있습니다. Git diff 가 전체 줄 변경으로 보이거나 일부 도구에서 줄이 합쳐질 수 있습니다', 'Mixed line endings can make Git diffs show every line as changed and some tools join lines'));
    if (cr && !crlf && !lf) notes.push('ℹ️ ' + t('CR 단독 줄바꿈은 Classic Mac OS(9 이하) 형식입니다. 요즘은 거의 쓰이지 않습니다', 'A bare CR is the Classic Mac OS (9 and earlier) format and is rarely used today'));
    if (crlf && o.to === 'lf') notes.push('ℹ️ ' + t('셸 스크립트(.sh)는 CRLF 면 "bad interpreter: /bin/bash^M" 오류가 납니다. LF 로 저장하세요', 'A CRLF shell script fails with "bad interpreter: /bin/bash^M"; save it with LF'));
    if (hadBom && o.bom === 'keep') notes.push('ℹ️ ' + t('UTF-8 BOM 이 있습니다. 셸 스크립트·JSON·일부 파서에서는 BOM 이 문제를 일으킬 수 있습니다', 'A UTF-8 BOM is present and can break shell scripts, JSON and some parsers'));
    var changed = out !== text;
    return { _status: mixed ? { ok: 'info', msg: t('⚠️ 줄바꿈 혼용 — LF ' + lf + ' · CRLF ' + crlf + ' · CR ' + cr, '⚠️ Mixed endings - LF ' + lf + ' · CRLF ' + crlf + ' · CR ' + cr) } : t('✅ ' + (total ? dom : '줄바꿈 없음') + ' ' + total + '개' + (changed ? ' → 변환됨' : ''), '✅ ' + (total ? dom : 'no line breaks') + ' × ' + total + (changed ? ' → converted' : '')), info: info, lines: { head: [['줄바꿈 번호', 'Break #'], ['종류', 'Kind'], ['주된 종류', 'Dominant']], rows: rows, empty: ['혼용된 줄바꿈이 없습니다', 'No mixed line breaks'] }, out: out, issues: notes };
  }
});
