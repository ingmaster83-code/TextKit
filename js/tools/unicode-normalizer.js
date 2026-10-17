TK.tool('unicode-normalizer', {
  inputs: [
    { id: 'in', label: ['텍스트', 'Text'], rows: 5, sample: '한글 파일명(분해형): \u1112\u1161\u11AB\u1100\u1173\u11AF.txt\ncafé ﬁ ① ㈜ Ａ１ ½' },
    { id: 'b', label: ['비교할 텍스트 B (선택 — 정규화하면 같은지 확인)', 'Text B (optional — equal after normalisation?)'], rows: 2, sample: 'café' }
  ],
  options: [
    { id: 'form', type: 'select', label: ['변환 형식', 'Form'], choices: [['NFC', ['NFC — 조합형 (한글은 완성형, 기본 추천)', 'NFC - composed (recommended)']], ['NFD', ['NFD — 분해형 (macOS 파일명)', 'NFD - decomposed (macOS file names)']], ['NFKC', ['NFKC — 호환 문자까지 통일 (전각·원문자·합자)', 'NFKC - also folds compatibility characters']], ['NFKD', ['NFKD — 호환 + 분해', 'NFKD - compatibility + decomposed']]], default: 'NFC' },
    { id: 'diff', type: 'checkbox', label: ['바뀐 글자만 표로 보기', 'List only characters that changed'], default: true }
  ],
  outputs: [{ id: 'forms', label: ['4가지 형식 비교', 'All four forms'], kind: 'table' }, { id: 'changes', label: ['바뀐 글자', 'Changed characters'], kind: 'table' }, { id: 'out', label: ['변환 결과', 'Result'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var text = String(v['in'] == null ? '' : v['in']); if (!text.length) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    var F = ['NFC', 'NFD', 'NFKC', 'NFKD'];
    function hex(c) { return 'U+' + ('0000' + c.codePointAt(0).toString(16).toUpperCase()).slice(-4); }
    function cpsOf(s, max) { var a = Array.from(s).map(hex); return a.length > (max || 10) ? a.slice(0, max || 10).join(' ') + ' …' : a.join(' '); }
    var out = text.normalize(o.form), notes = [];
    var forms = F.map(function (f) { var n = text.normalize(f); return [f, String(Array.from(n).length), String(n.length), String(new TextEncoder().encode(n).length), n === text ? '= ' + t('원본과 같음', 'same as input') : t('다름', 'differs')]; });
    var changes = [];
    Array.from(text).forEach(function (ch, i) {
      var n = ch.normalize(o.form);
      if (n !== ch || !o.diff) {
        if (n !== ch || (!o.diff && i < 500)) changes.push([String(i + 1), ch, cpsOf(ch), n, cpsOf(n), n === ch ? '—' : (Array.from(n).length > 1 ? t('분해', 'decomposed') : t('다른 문자로 대체', 'replaced'))]);
      }
    });
    /* 조합 시퀀스(기본 문자 + 결합 부호)가 합쳐지는 경우도 보여 주기: 문자소 단위 */
    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      var seen = {};
      Array.from(new Intl.Segmenter(undefined, { granularity: 'grapheme' }).segment(text), function (s) { return s.segment; }).forEach(function (g, i) {
        var n = g.normalize(o.form);
        if (n !== g && Array.from(g).length > 1 && Array.from(n).length < Array.from(g).length && !seen[g]) { seen[g] = 1; changes.push([String(i + 1) + ' (' + t('문자소', 'cluster') + ')', g, cpsOf(g), n, cpsOf(n), t('합침', 'composed')]); }
      });
    }
    var b = String(v.b == null ? '' : v.b);
    if (b.trim()) {
      /* A 의 각 줄을 B 와 비교해 가장 가까운 관계를 찾는다 (같음 > NFC 같음 > NFKC 같음) */
      var rel = 0, relLine = 0; // 3 = 동일, 2 = NFC, 1 = NFKC
      var cands = []; text.split(/\r?\n/).forEach(function (ln, idx) { cands.push([ln, idx + 1]); ln.split(/[\s/:()]+/).forEach(function (w) { if (w) cands.push([w, idx + 1]); }); });
      cands.forEach(function (cd) { var ln = cd[0], idx = cd[1] - 1; var r = ln === b ? 3 : ln.normalize('NFC') === b.normalize('NFC') ? 2 : ln.normalize('NFKC') === b.normalize('NFKC') ? 1 : 0; if (r > rel) { rel = r; relLine = idx + 1; } });
      if (rel === 3) notes.push('✅ ' + t('A 의 ' + relLine + '번째 줄과 B 는 코드 포인트까지 완전히 같습니다', 'Line ' + relLine + ' of A and B are identical down to the code points'));
      else if (rel === 2) notes.push('⚠️ ' + t('A 의 ' + relLine + '번째 줄과 B 는 화면에서는 같아 보이지만 코드 포인트가 다릅니다. NFC 로 정규화하면 같아집니다 (비교·검색·중복 제거 전에 NFC 로 통일하세요)', 'Line ' + relLine + ' of A and B look the same but differ in code points; they become equal under NFC (normalise to NFC before comparing, searching or deduplicating)'));
      else if (rel === 1) notes.push('⚠️ ' + t('A 의 ' + relLine + '번째 줄과 B 는 NFKC(호환 정규화)로만 같아집니다 (전각·합자·원문자 차이)', 'Line ' + relLine + ' of A and B only become equal under NFKC (fullwidth / ligature / enclosed differences)'));
      else notes.push('ℹ️ ' + t('A 의 어느 줄도 B 와 정규화 형식으로 같아지지 않습니다', 'No line of A equals B under any normalisation form'));
    }
    var jamo = /[ᄀ-ᇿ]/.test(text) || /[ᄀ-ᇿ]/.test(text.normalize('NFD')) && text.normalize('NFC') !== text.normalize('NFD');
    if (/[ᄀ-ᇿ]/.test(text) && o.form !== 'NFD' && o.form !== 'NFKD') notes.push('ℹ️ ' + t('입력에 분해된 한글 자모(U+1100 대역)가 있습니다. macOS 파일명이나 일부 PDF·클립보드에서 생기며 NFC 로 합치면 완성형 한글이 됩니다', 'The input contains decomposed Hangul jamo (U+1100 block), typical of macOS file names and some PDFs; NFC recomposes them into syllables'));
    if (/[가-힣]/.test(text) && (o.form === 'NFD' || o.form === 'NFKD')) notes.push('ℹ️ ' + t('한글 완성형이 자모로 분해되어 길이가 늘어납니다 (음절 1자 → 자모 2~3개). 글자수·정렬 결과가 달라질 수 있습니다', 'Hangul syllables are split into jamo, so the length grows (1 syllable → 2-3 jamo) and counting / sorting results change'));
    if ((o.form === 'NFKC' || o.form === 'NFKD') && out !== text.normalize('NFC')) notes.push('ℹ️ ' + t('NFKC/NFKD 는 의미를 일부 잃을 수 있습니다 (예: ① → 1, ㈜ → (주), ½ → 1⁄2, ﬁ → fi). 사용자 입력을 저장할 때는 보통 NFC 를 씁니다', 'NFKC / NFKD can lose information (e.g. ① → 1, ㈜ → (주), ½ → 1⁄2, ﬁ → fi); NFC is the usual choice for storing user input'));
    if (out === text) notes.push('✅ ' + t('이미 ' + o.form + ' 형식입니다', 'The text is already in ' + o.form));
    return { _status: out === text ? t('✅ 이미 ' + o.form, '✅ Already ' + o.form) : t('✅ ' + o.form + ' 로 변환: ' + Array.from(text).length + ' → ' + Array.from(out).length + '자', '✅ Converted to ' + o.form + ': ' + Array.from(text).length + ' → ' + Array.from(out).length + ' code points'), forms: { head: [['형식', 'Form'], ['코드 포인트', 'Code points'], ['UTF-16 길이', 'UTF-16 length'], ['UTF-8 바이트', 'UTF-8 bytes'], ['원본 비교', 'vs input']], rows: forms }, changes: { head: [['위치', 'Position'], ['원본', 'Original'], ['원본 코드', 'Original code'], ['변환', 'Result'], ['변환 코드', 'Result code'], ['종류', 'Kind']], rows: changes.slice(0, 500), empty: ['바뀐 글자가 없습니다', 'Nothing changed'] }, out: out, issues: notes };
  }
});
