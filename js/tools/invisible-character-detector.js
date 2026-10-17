TK.tool('invisible-character-detector', {
  inputs: [{ id: 'in', label: ['검사할 텍스트', 'Text to check'], rows: 8, sample: 'Hello​World, price is 100　won.\nuser‮admin‬ = "ok";­ soft⁠ joined‍ text﻿ㅤ' }],
  options: [
    { id: 'action', type: 'select', label: ['정리 방식', 'Cleaning'], choices: [['remove', ['모두 제거 (공백류는 일반 공백으로)', 'Remove all (space-like → ASCII space)']], ['spaces', ['공백류만 일반 공백으로 바꾸고 나머지는 유지', 'Only turn space-like characters into ASCII spaces']], ['mark', ['제거하지 않고 [U+XXXX] 로 표시', 'Keep but mark as [U+XXXX]']]], default: 'remove' },
    { id: 'emoji', type: 'checkbox', label: ['이모지 결합용 ZWJ·변형 선택자(VS16)는 정상으로 간주', 'Treat emoji ZWJ and variation selectors as normal'], default: true },
    { id: 'bomstart', type: 'checkbox', label: ['맨 앞의 BOM(FEFF)은 제외', 'Ignore a BOM at the very start'], default: false }
  ],
  outputs: [{ id: 'table', label: ['발견된 문자', 'Found characters'], kind: 'table' }, { id: 'sum', label: ['종류별 개수', 'Count by kind'], kind: 'table' }, { id: 'marked', label: ['위치 표시', 'Marked text'], kind: 'code', ext: 'txt' }, { id: 'out', label: ['정리된 텍스트', 'Cleaned text'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var text = String(v['in'] == null ? '' : v['in']); if (!text.length) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    var K = {};
    function def(cp, name, kind, risk, space) { K[cp] = { name: name, kind: kind, risk: risk, space: !!space }; }
    def(0x00A0, 'NO-BREAK SPACE', 'space', 'low', true); def(0x1680, 'OGHAM SPACE MARK', 'space', 'low', true);
    for (var s = 0x2000; s <= 0x200A; s++) def(s, ['EN QUAD', 'EM QUAD', 'EN SPACE', 'EM SPACE', 'THREE-PER-EM SPACE', 'FOUR-PER-EM SPACE', 'SIX-PER-EM SPACE', 'FIGURE SPACE', 'PUNCTUATION SPACE', 'THIN SPACE', 'HAIR SPACE'][s - 0x2000], 'space', 'low', true);
    def(0x202F, 'NARROW NO-BREAK SPACE', 'space', 'low', true); def(0x205F, 'MEDIUM MATHEMATICAL SPACE', 'space', 'low', true); def(0x3000, 'IDEOGRAPHIC SPACE', 'space', 'low', true);
    def(0x200B, 'ZERO WIDTH SPACE', 'zero', 'high'); def(0x200C, 'ZERO WIDTH NON-JOINER', 'zero', 'medium'); def(0x200D, 'ZERO WIDTH JOINER', 'zero', 'medium'); def(0x2060, 'WORD JOINER', 'zero', 'medium'); def(0xFEFF, 'ZERO WIDTH NO-BREAK SPACE / BOM', 'zero', 'medium');
    def(0x00AD, 'SOFT HYPHEN', 'format', 'medium'); def(0x180E, 'MONGOLIAN VOWEL SEPARATOR', 'zero', 'medium');
    def(0x200E, 'LEFT-TO-RIGHT MARK', 'bidi', 'medium'); def(0x200F, 'RIGHT-TO-LEFT MARK', 'bidi', 'medium'); def(0x061C, 'ARABIC LETTER MARK', 'bidi', 'medium');
    ['LEFT-TO-RIGHT EMBEDDING', 'RIGHT-TO-LEFT EMBEDDING', 'POP DIRECTIONAL FORMATTING', 'LEFT-TO-RIGHT OVERRIDE', 'RIGHT-TO-LEFT OVERRIDE'].forEach(function (n, i) { def(0x202A + i, n, 'bidi', 'critical'); });
    ['LEFT-TO-RIGHT ISOLATE', 'RIGHT-TO-LEFT ISOLATE', 'FIRST STRONG ISOLATE', 'POP DIRECTIONAL ISOLATE'].forEach(function (n, i) { def(0x2066 + i, n, 'bidi', 'critical'); });
    ['FUNCTION APPLICATION', 'INVISIBLE TIMES', 'INVISIBLE SEPARATOR', 'INVISIBLE PLUS'].forEach(function (n, i) { def(0x2061 + i, n, 'format', 'medium'); });
    def(0x115F, 'HANGUL CHOSEONG FILLER', 'filler', 'high'); def(0x1160, 'HANGUL JUNGSEONG FILLER', 'filler', 'high'); def(0x3164, 'HANGUL FILLER', 'filler', 'high'); def(0xFFA0, 'HALFWIDTH HANGUL FILLER', 'filler', 'high'); def(0x2800, 'BRAILLE PATTERN BLANK', 'filler', 'high'); def(0x17B4, 'KHMER VOWEL INHERENT AQ', 'filler', 'high'); def(0x17B5, 'KHMER VOWEL INHERENT AA', 'filler', 'high');
    def(0x2028, 'LINE SEPARATOR', 'linebreak', 'medium'); def(0x2029, 'PARAGRAPH SEPARATOR', 'linebreak', 'medium'); def(0x0085, 'NEXT LINE (NEL)', 'linebreak', 'medium');
    def(0xFFFC, 'OBJECT REPLACEMENT CHARACTER', 'format', 'medium'); def(0xFFFD, 'REPLACEMENT CHARACTER (깨진 문자 자리)', 'broken', 'medium');
    def(0x034F, 'COMBINING GRAPHEME JOINER', 'zero', 'medium'); def(0x2063, 'INVISIBLE SEPARATOR', 'format', 'medium');
    var KIND_KO = { space: '특수 공백', zero: '제로폭 문자', format: '서식 문자', bidi: '방향 제어', filler: '빈 글자(필러)', linebreak: '특수 줄바꿈', control: '제어 문자', tag: '태그 문자', vs: '변형 선택자', broken: '깨진 문자' };
    var KIND_EN = { space: 'Unusual space', zero: 'Zero-width', format: 'Format character', bidi: 'Bidi control', filler: 'Blank filler', linebreak: 'Unusual line break', control: 'Control character', tag: 'Tag character', vs: 'Variation selector', broken: 'Broken character' };
    var RISK_KO = { low: '낮음', medium: '중간', high: '높음', critical: '심각' };
    function info(cp) {
      if (K[cp]) return K[cp];
      if (cp < 0x20 && cp !== 9 && cp !== 10 && cp !== 13) return { name: 'C0 CONTROL U+' + ('0000' + cp.toString(16).toUpperCase()).slice(-4), kind: 'control', risk: 'medium', space: false };
      if (cp === 0x7F || (cp >= 0x80 && cp <= 0x9F && cp !== 0x85)) return { name: 'CONTROL U+' + ('0000' + cp.toString(16).toUpperCase()).slice(-4), kind: 'control', risk: 'medium', space: false };
      if (cp >= 0xE0000 && cp <= 0xE007F) return { name: 'TAG CHARACTER U+' + cp.toString(16).toUpperCase(), kind: 'tag', risk: 'high', space: false };
      if ((cp >= 0xFE00 && cp <= 0xFE0F) || (cp >= 0xE0100 && cp <= 0xE01EF)) return { name: 'VARIATION SELECTOR U+' + cp.toString(16).toUpperCase(), kind: 'vs', risk: 'low', space: false };
      return null;
    }
    var skippedEmoji = 0, rows = [], counts = {}, marked = '', cleaned = '', line = 1, col = 0, cps = Array.from(text), prevCp = 0;
    var EMOJI = /\p{Extended_Pictographic}|\p{Emoji_Modifier}|⃣/u;
    cps.forEach(function (ch, idx) {
      var cp = ch.codePointAt(0), inf = info(cp), flagged = !!inf;
      col++;
      if (ch === '\n') { line++; col = 0; }
      if (flagged) {
        var nextCh = cps[idx + 1] || '';
        var emojiCtx = o.emoji && (cp === 0x200D || inf.kind === 'vs') && (EMOJI.test(cps[idx - 1] || '') || EMOJI.test(nextCh) || cp === 0xFE0F);
        if (o.bomstart && cp === 0xFEFF && idx === 0) flagged = false;
        if (emojiCtx && (cp === 0x200D || (inf.kind === 'vs' && cp !== 0xFE0E))) flagged = false;
        if (emojiCtx && cp === 0x200D) flagged = false;
      }
      if (!flagged) { if (inf && (cp === 0x200D || inf.kind === 'vs')) skippedEmoji++; marked += ch; cleaned += ch; prevCp = cp; return; }
      var key = 'U+' + ('0000' + cp.toString(16).toUpperCase()).slice(-4);
      counts[key] = counts[key] || { n: 0, inf: inf }; counts[key].n++;
      rows.push([line + ':' + col, key, inf.name, t(KIND_KO[inf.kind], KIND_EN[inf.kind]), t(RISK_KO[inf.risk], inf.risk), String(cps.slice(Math.max(0, idx - 6), idx).join('').replace(/\n/g, '↵')) + ' ▮ ' + String(cps.slice(idx + 1, idx + 7).join('').replace(/\n/g, '↵'))]);
      marked += '[' + key + ']';
      if (o.action === 'remove') { if (inf.space) cleaned += ' '; }
      else if (o.action === 'spaces') { cleaned += inf.space ? ' ' : ch; }
      else cleaned += '[' + key + ']';
      prevCp = cp;
    });
    var sum = Object.keys(counts).map(function (k) { return [k, counts[k].inf.name, String(counts[k].n), t(RISK_KO[counts[k].inf.risk], counts[k].inf.risk)]; });
    var notes = [];
    var bidi = rows.filter(function (r) { return r[3] === t(KIND_KO.bidi, KIND_EN.bidi) && /U\+(202[A-E]|206[6-9])/.test(r[1]); }).length;
    if (bidi) notes.push('⛔ ' + t('방향 덮어쓰기/격리 제어 문자 ' + bidi + '개: 소스 코드나 파일 이름에 있으면 보이는 모양과 실제 내용이 달라지는 "Trojan Source" 공격에 쓰일 수 있습니다 (CVE-2021-42574)', bidi + ' bidirectional override / isolate control(s): in source code or file names they can make the visible text differ from the real content ("Trojan Source", CVE-2021-42574)'));
    if (rows.some(function (r) { return /U\+(200B|2060|FEFF)$/.test(r[1]) && true; })) notes.push('⚠️ ' + t('제로폭 문자는 눈에 보이지 않아 복사한 코드·비밀번호·URL 이 동작하지 않는 흔한 원인입니다', 'Zero-width characters are invisible and a common reason why copied code, passwords or URLs stop working'));
    if (rows.some(function (r) { return /U\+(3164|115F|1160|FFA0|2800)$/.test(r[1]); })) notes.push('⚠️ ' + t('한글 필러·점자 공백은 "빈 글자"처럼 보이지만 공백 검사를 통과해 닉네임·ID 위장에 악용됩니다', 'Hangul fillers and the Braille blank look empty but pass whitespace checks, so they are abused to fake empty names / IDs'));
    if (rows.some(function (r) { return /U\+FFFD$/.test(r[1]); })) notes.push('ℹ️ ' + t('대체 문자(�)는 인코딩이 깨졌다는 표시입니다. "인코딩 복구 도구"로 원인을 찾아보세요', 'The replacement character (�) marks broken encoding; try the encoding repair tool'));
    if (skippedEmoji) notes.push('ℹ️ ' + t('이모지에 쓰인 ZWJ(200D)와 변형 선택자(FE0F) ' + skippedEmoji + '개는 정상 사용으로 보고 제외했습니다', skippedEmoji + ' ZWJ / variation selector(s) used in emoji sequences were treated as normal'));
    if (!rows.length) notes.push('✅ ' + t('보이지 않는 문자나 특수 공백이 없습니다', 'No invisible characters or unusual spaces found'));
    if (o.action === 'remove') notes.push('ℹ️ ' + t('한글 필러(3164)·점자 공백은 공백으로 바꾸지 않고 제거합니다', 'Hangul fillers and the Braille blank are removed, not replaced with spaces'));
    return { _status: rows.length ? { ok: 'info', msg: t('⚠️ 의심 문자 ' + rows.length + '개 (' + sum.length + '종류)', '⚠️ ' + rows.length + ' suspicious character(s) (' + sum.length + ' kind(s))') } : t('✅ 깨끗합니다', '✅ Clean'), table: { head: [['위치(줄:열)', 'Position'], ['코드', 'Code'], ['이름', 'Name'], ['분류', 'Kind'], ['위험도', 'Risk'], ['앞뒤 문맥', 'Context']], rows: rows.slice(0, 1000), empty: ['발견된 문자가 없습니다', 'Nothing found'] }, sum: { head: [['코드', 'Code'], ['이름', 'Name'], ['개수', 'Count'], ['위험도', 'Risk']], rows: sum }, marked: marked, out: cleaned, issues: notes };
  }
});
