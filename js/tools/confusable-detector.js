TK.tool('confusable-detector', {
  sampleExpectError: true,
  inputs: [
    { id: 'in', label: ['검사할 텍스트 (도메인, 사용자 이름, 코드 등)', 'Text to check (domain, username, code ...)'], rows: 6, sample: 'раураl.com\nadmin 계정: аdmіn\nwooahouse.com\nＰａｙＰａｌ\nl0gin Ο1' },
    { id: 'b', label: ['비교할 텍스트 B (선택 — 겉모양이 같은지 확인)', 'Text B to compare with (optional — same look?)'], rows: 2, sample: 'paypal.com' }
  ],
  options: [
    { id: 'mixed', type: 'checkbox', label: ['한 단어 안의 스크립트 혼용(예: 라틴+키릴)도 검사', 'Also flag mixed scripts inside one word (e.g. Latin + Cyrillic)'], default: true },
    { id: 'ambig', type: 'checkbox', label: ['글꼴에 따라 헷갈리는 ASCII(l/I/1, O/0)도 표시', 'Also flag ASCII look-alikes in some fonts (l/I/1, O/0)'], default: true }
  ],
  sampleOptions: { mixed: true },
  outputs: [{ id: 'table', label: ['의심 문자', 'Suspicious characters'], kind: 'table' }, { id: 'words', label: ['단어별 스크립트', 'Scripts per word'], kind: 'table' }, { id: 'skel', label: ['스켈레톤 (겉모양을 ASCII 로 환원)', 'Skeleton (look-alikes mapped to ASCII)'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['판정', 'Verdict'], kind: 'list' }],
  run: function (v, o, t) {
    var text = String(v['in'] == null ? '' : v['in']); if (!text.trim()) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    /* 자주 쓰이는 라틴 닮은꼴 (원본 문자 → ASCII). Unicode confusables 의 핵심 부분집합 */
    var MAP = {};
    function add(fromChars, toChars) { var f = Array.from(fromChars), tt = Array.from(toChars); f.forEach(function (c, i) { MAP[c] = tt[i]; }); }
    /* 키릴 */
    add('аеорсухіјѕһԁԛԝѵАВЕКМНОРСТХІЈЅҮЗԌӀ', 'aeopcyxijshdqwvABEKMHOPCTXIJSY3Gl');
    add('ѡ', 'w'); add('ԍ', 'g'); add('ӏ', 'l'); add('ɡ', 'g'); add('ԑ', 'e'); add('ѕ', 's');
    /* 그리스 */
    add('οανρυικχΑΒΕΖΗΙΚΜΝΟΡΤΥΧϹϳ', 'oavpuikxABEZHIKMNOPTYXCj');
    add('ɑ', 'a'); add('ƅ', 'b'); add('ᴄ', 'c'); add('ᴅ', 'd'); add('ᴇ', 'e'); add('ᴍ', 'm'); add('ᴏ', 'o'); add('ᴘ', 'p'); add('ᴛ', 't'); add('ᴜ', 'u'); add('ᴠ', 'v'); add('ᴡ', 'w'); add('ᴢ', 'z');
    /* 라틴 확장·기타 */
    add('ıȷǀ|Ⅰⅼ∣', 'ijlIIll'); add('Ο０', 'O0'); add('ǃ', '!'); add('‐‑‒–−', '-----'); add('’‘ʼ′´`', "''''''"); add('“”″', '"""'); add('․﹒', '..'); add('∕⁄／', '///'); add('﹕꞉', '::'); add('＿', '_');
    /* 한글·CJK 에서 흔한 닮은꼴 */
    add('ㅇㅡㅣ〇一丨', 'o-l0-l'); add('、。', ',.');
    var AMBIG = { 'l': 'I/1', 'I': 'l/1', '1': 'l/I', 'O': '0', '0': 'O', 'o': '0', 'S': '5', '5': 'S', 'B': '8', '8': 'B', 'rn': 'm', 'vv': 'w' };
    var SCRIPTS = ['Latin', 'Greek', 'Cyrillic', 'Armenian', 'Hebrew', 'Arabic', 'Devanagari', 'Thai', 'Hangul', 'Han', 'Hiragana', 'Katakana', 'Cherokee', 'Georgian', 'Ethiopic'];
    var SC_RE = SCRIPTS.map(function (s) { return [s, new RegExp('^\\p{Script=' + s + '}$', 'u')]; });
    function scriptOf(ch) {
      for (var i = 0; i < SC_RE.length; i++) if (SC_RE[i][1].test(ch)) return SC_RE[i][0];
      if (/^\p{Script=Common}$/u.test(ch)) return 'Common'; if (/^\p{Script=Inherited}$/u.test(ch)) return 'Inherited';
      return 'Other';
    }
    function hex(c) { return 'U+' + ('0000' + c.codePointAt(0).toString(16).toUpperCase()).slice(-4); }
    function skeleton(s) {
      var out = '';
      Array.from(s).forEach(function (c) { out += MAP[c] !== undefined ? MAP[c] : c.normalize('NFKC'); });
      return out.normalize('NFKC').replace(/[̀-ͯ]/g, function () { return ''; });
    }
    var rows = [], notes = [], wordRows = [], cps = Array.from(text), pos = 0, line = 1, col = 0;
    cps.forEach(function (ch) {
      col++; if (ch === '\n') { line++; col = 0; return; }
      var cp = ch.codePointAt(0), sc = scriptOf(ch), why = '', look = '', sev = '';
      if (MAP[ch] !== undefined && cp > 127) { look = MAP[ch]; why = t('ASCII "' + look + '" 와 겉모양이 비슷합니다', 'Looks like ASCII "' + look + '"'); sev = sc === 'Hangul' || sc === 'Han' ? 'info' : 'warn'; }
      else if (cp > 0xFF00 && cp < 0xFF5F) { look = String.fromCharCode(cp - 0xFEE0); why = t('전각(Fullwidth) 문자 — ASCII "' + look + '" 의 전각 형태', 'Fullwidth form of ASCII "' + look + '"'); sev = 'warn'; }
      else if (ch.normalize('NFKC') !== ch && /[\u{1D400}-\u{1D7FF}①-⓿℀-⅏]/u.test(ch)) { look = ch.normalize('NFKC'); why = t('수학/원문자 서식 문자 — NFKC 로 "' + look + '"', 'Mathematical / enclosed form — "' + look + '" under NFKC'); sev = 'warn'; }
      else if (o.ambig && /[lI1O0oS5B8]/.test(ch) && cp < 128) { /* 아래에서 단어 단위로 */ }
      if (why) rows.push([line + ':' + col, ch, hex(ch), sc, look, why, sev === 'warn' ? '⚠️' : 'ℹ️']);
    });
    /* 단어(공백·구두점 경계) 단위 스크립트 혼용 */
    var words = text.split(/[\s,;()\[\]{}"'<>]+/).filter(Boolean), mixedBad = 0;
    words.forEach(function (w) {
      var set = {}; Array.from(w).forEach(function (c) { var s = scriptOf(c); if (s !== 'Common' && s !== 'Inherited') set[s] = (set[s] || 0) + 1; });
      var names = Object.keys(set);
      var allowed = [['Han', 'Hiragana', 'Katakana'], ['Han', 'Hangul'], ['Han', 'Latin'], ['Hangul', 'Latin'], ['Latin', 'Hiragana', 'Katakana', 'Han']];
      var ok = names.length <= 1 || allowed.some(function (g) { return names.every(function (n) { return g.indexOf(n) >= 0; }); });
      var bad = names.length > 1 && !ok;
      if (o.mixed && bad) mixedBad++;
      var puny = ''; if (/^[^\s/]+\.[^\s/]+$/.test(w) && /[^\x00-\x7F]/.test(w)) { try { puny = new URL('http://' + w).hostname; } catch (e) { puny = ''; } }
      if (names.length > 1 || puny) wordRows.push([w, names.map(function (n) { return n + ' ' + set[n]; }).join(' + ') || '—', bad ? '⚠️ ' + t('혼용', 'mixed') : (names.length > 1 ? 'ℹ️ ' + t('허용되는 조합', 'allowed combination') : '—'), puny || '—']);
    });
    /* 헷갈리는 ASCII */
    var ambigRows = [];
    if (o.ambig) words.forEach(function (w) {
      if (/^[A-Za-z0-9_.@-]+$/.test(w) && /(?=.*[lI1])(?=.*[A-Za-z])/.test(w) && /[lI1]/.test(w) && /[A-Za-z]/.test(w) && w.length > 2 && /[lI]/.test(w) && /(?:[a-z][1I]|[1I][a-z]|[lI][01O]|[01O][lI]|I1|l1|1l|1I|0O|O0|lI|Il)/.test(w)) ambigRows.push(w);
      else if (/[A-Za-z]/.test(w) && /[0O]/.test(w) && /(?:[a-z]0[a-z]|\b0[a-z]|[a-z]0\b)/.test(w)) ambigRows.push(w);
    });
    /* 비교 */
    var b = String(v.b == null ? '' : v.b).trim(), verdict = [];
    var skel = skeleton(text);
    var skelA = text.split('\n').map(skeleton);
    if (b) {
      var sa = skeleton(text.split('\n')[0] || text).toLowerCase(), sb = skeleton(b).toLowerCase();
      var firstLine = text.split('\n')[0];
      if (firstLine === b) verdict.push('✅ ' + t('A 의 첫 줄과 B 가 완전히 같습니다', 'The first line of A and B are identical'));
      else if (sa === sb) verdict.push('⛔ ' + t('A 의 첫 줄과 B 는 글자는 다르지만 겉모양(스켈레톤)이 같습니다 — 스푸핑(동형 이의 문자) 가능성이 높습니다', 'The first line of A and B differ in code points but have the same skeleton - a likely homograph spoof'));
      else verdict.push('✅ ' + t('A 의 첫 줄과 B 는 겉모양도 다릅니다', 'The first line of A and B look different too'));
    }
    var nWarn = rows.filter(function (r) { return r[6] === '⚠️'; }).length;
    if (nWarn) notes.push('⚠️ ' + t('ASCII 와 닮은 비ASCII 문자 ' + nWarn + '개가 있습니다. 도메인·사용자 이름·소스 코드에 있으면 피싱이나 계정 위장에 악용될 수 있습니다', nWarn + ' non-ASCII look-alike character(s) found; in domains, usernames or source code they enable phishing and impersonation'));
    if (mixedBad) notes.push('⛔ ' + t('한 단어 안에 서로 다른 스크립트가 섞인 단어가 ' + mixedBad + '개 있습니다. 브라우저도 이런 도메인은 punycode(xn--)로 표시해 경고합니다', mixedBad + ' word(s) mix different scripts; browsers show such domains in punycode (xn--) as a warning'));
    if (ambigRows.length) notes.push('ℹ️ ' + t('글꼴에 따라 l/I/1, O/0 이 헷갈릴 수 있는 단어: ' + ambigRows.slice(0, 6).join(', '), 'Words with characters that can look alike in some fonts (l/I/1, O/0): ' + ambigRows.slice(0, 6).join(', ')));
    wordRows.filter(function (r) { return r[3] !== '—'; }).forEach(function (r) { notes.push('ℹ️ ' + t('도메인 형태 "' + r[0] + '" 의 punycode: ' + r[3], 'Domain-like "' + r[0] + '" in punycode: ' + r[3])); });
    verdict.forEach(function (x) { notes.unshift(x); });
    if (!rows.length && !mixedBad && !verdict.length) notes.push('✅ ' + t('동형 이의 문자나 스크립트 혼용이 발견되지 않았습니다', 'No homoglyphs or mixed scripts found'));
    notes.push('ℹ️ ' + t('닮은꼴 표는 자주 악용되는 문자 위주의 부분집합입니다. 유니코드 컨퓨저블 전체 데이터는 포함하지 않으므로 중요한 판단에는 punycode 표시와 함께 확인하세요', 'The look-alike table covers the commonly abused characters, not the entire Unicode confusables data; confirm important decisions with the punycode form'));
    var bad = rows.some(function (r) { return r[6] === '⚠️'; }) || mixedBad > 0 || verdict.some(function (x) { return x.indexOf('⛔') === 0; });
    return { _status: bad ? { ok: false, msg: t('⛔ 의심스러운 문자 ' + rows.length + '개 · 혼용 단어 ' + mixedBad + '개', '⛔ ' + rows.length + ' suspicious character(s) · ' + mixedBad + ' mixed word(s)') } : t('✅ 의심스러운 문자가 없습니다', '✅ No suspicious characters'), table: { head: [['위치(줄:열)', 'Position'], ['글자', 'Char'], ['코드', 'Code'], ['스크립트', 'Script'], ['닮은 글자', 'Looks like'], ['설명', 'Why'], ['', '']], rows: rows.slice(0, 500), empty: ['의심 문자가 없습니다', 'Nothing suspicious'] }, words: { head: [['단어', 'Word'], ['스크립트 구성', 'Scripts'], ['판정', 'Verdict'], ['punycode', 'punycode']], rows: wordRows, empty: ['스크립트가 섞인 단어가 없습니다', 'No mixed-script words'] }, skel: skelA.join('\n'), issues: notes };
  }
});
