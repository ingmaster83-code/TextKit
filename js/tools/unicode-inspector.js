TK.tool('unicode-inspector', {
  inputs: [{ id: 'in', label: ['검사할 텍스트', 'Text to inspect'], rows: 6, sample: 'Hello, 안녕! café 👨‍👩‍👧 한글​ Á ①' }],
  options: [
    { id: 'limit', type: 'number', label: ['표시할 최대 코드 포인트 수', 'Max code points to list'], default: 300, min: 10, max: 5000 },
    { id: 'hide', type: 'checkbox', label: ['ASCII 영문·숫자는 표에서 숨김', 'Hide ASCII letters and digits'], default: false }
  ],
  outputs: [{ id: 'info', label: ['요약', 'Summary'], kind: 'kv' }, { id: 'table', label: ['코드 포인트별 정보', 'Per code point'], kind: 'table' }, { id: 'gr', label: ['문자소(Grapheme) 단위', 'Grapheme clusters'], kind: 'table' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var text = String(v['in'] == null ? '' : v['in']); if (!text.length) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    var NAMES = { 0: 'NULL', 7: 'BELL', 8: 'BACKSPACE', 9: 'CHARACTER TABULATION', 10: 'LINE FEED', 11: 'LINE TABULATION', 12: 'FORM FEED', 13: 'CARRIAGE RETURN', 27: 'ESCAPE', 32: 'SPACE', 33: 'EXCLAMATION MARK', 34: 'QUOTATION MARK', 35: 'NUMBER SIGN', 36: 'DOLLAR SIGN', 37: 'PERCENT SIGN', 38: 'AMPERSAND', 39: 'APOSTROPHE', 40: 'LEFT PARENTHESIS', 41: 'RIGHT PARENTHESIS', 42: 'ASTERISK', 43: 'PLUS SIGN', 44: 'COMMA', 45: 'HYPHEN-MINUS', 46: 'FULL STOP', 47: 'SOLIDUS', 58: 'COLON', 59: 'SEMICOLON', 60: 'LESS-THAN SIGN', 61: 'EQUALS SIGN', 62: 'GREATER-THAN SIGN', 63: 'QUESTION MARK', 64: 'COMMERCIAL AT', 91: 'LEFT SQUARE BRACKET', 92: 'REVERSE SOLIDUS', 93: 'RIGHT SQUARE BRACKET', 94: 'CIRCUMFLEX ACCENT', 95: 'LOW LINE', 96: 'GRAVE ACCENT', 123: 'LEFT CURLY BRACKET', 124: 'VERTICAL LINE', 125: 'RIGHT CURLY BRACKET', 126: 'TILDE', 127: 'DELETE', 133: 'NEXT LINE', 160: 'NO-BREAK SPACE', 169: 'COPYRIGHT SIGN', 173: 'SOFT HYPHEN', 174: 'REGISTERED SIGN', 176: 'DEGREE SIGN', 177: 'PLUS-MINUS SIGN', 183: 'MIDDLE DOT', 215: 'MULTIPLICATION SIGN', 247: 'DIVISION SIGN', 768: 'COMBINING GRAVE ACCENT', 769: 'COMBINING ACUTE ACCENT', 770: 'COMBINING CIRCUMFLEX ACCENT', 771: 'COMBINING TILDE', 776: 'COMBINING DIAERESIS', 8192: 'EN QUAD', 8193: 'EM QUAD', 8194: 'EN SPACE', 8195: 'EM SPACE', 8196: 'THREE-PER-EM SPACE', 8197: 'FOUR-PER-EM SPACE', 8198: 'SIX-PER-EM SPACE', 8199: 'FIGURE SPACE', 8200: 'PUNCTUATION SPACE', 8201: 'THIN SPACE', 8202: 'HAIR SPACE', 8203: 'ZERO WIDTH SPACE', 8204: 'ZERO WIDTH NON-JOINER', 8205: 'ZERO WIDTH JOINER', 8206: 'LEFT-TO-RIGHT MARK', 8207: 'RIGHT-TO-LEFT MARK', 8208: 'HYPHEN', 8209: 'NON-BREAKING HYPHEN', 8211: 'EN DASH', 8212: 'EM DASH', 8216: 'LEFT SINGLE QUOTATION MARK', 8217: 'RIGHT SINGLE QUOTATION MARK', 8220: 'LEFT DOUBLE QUOTATION MARK', 8221: 'RIGHT DOUBLE QUOTATION MARK', 8226: 'BULLET', 8230: 'HORIZONTAL ELLIPSIS', 8232: 'LINE SEPARATOR', 8233: 'PARAGRAPH SEPARATOR', 8239: 'NARROW NO-BREAK SPACE', 8288: 'WORD JOINER', 8364: 'EURO SIGN', 8482: 'TRADE MARK SIGN', 8592: 'LEFTWARDS ARROW', 8593: 'UPWARDS ARROW', 8594: 'RIGHTWARDS ARROW', 8595: 'DOWNWARDS ARROW', 8734: 'INFINITY', 8800: 'NOT EQUAL TO', 9312: 'CIRCLED DIGIT ONE', 9313: 'CIRCLED DIGIT TWO', 9731: 'SNOWMAN', 9733: 'BLACK STAR', 10003: 'CHECK MARK', 10004: 'HEAVY CHECK MARK', 12288: 'IDEOGRAPHIC SPACE', 12289: 'IDEOGRAPHIC COMMA', 12290: 'IDEOGRAPHIC FULL STOP', 65279: 'ZERO WIDTH NO-BREAK SPACE (BOM)', 65533: 'REPLACEMENT CHARACTER', 128512: 'GRINNING FACE', 128077: 'THUMBS UP SIGN', 128105: 'WOMAN', 128104: 'MAN', 128103: 'GIRL', 128102: 'BOY', 128640: 'ROCKET', 10084: 'HEAVY BLACK HEART', 65039: 'VARIATION SELECTOR-16', 65038: 'VARIATION SELECTOR-15' };
    var CHO = ['G', 'GG', 'N', 'D', 'DD', 'R', 'M', 'B', 'BB', 'S', 'SS', '', 'J', 'JJ', 'C', 'K', 'T', 'P', 'H'], JUNG = ['A', 'AE', 'YA', 'YAE', 'EO', 'E', 'YEO', 'YE', 'O', 'WA', 'WAE', 'OE', 'YO', 'U', 'WEO', 'WE', 'WI', 'YU', 'EU', 'YI', 'I'], JONG = ['', 'G', 'GG', 'GS', 'N', 'NJ', 'NH', 'D', 'L', 'LG', 'LM', 'LB', 'LS', 'LT', 'LP', 'LH', 'M', 'B', 'BS', 'S', 'SS', 'NG', 'J', 'C', 'K', 'T', 'P', 'H'];
    var GC = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Mn', 'Mc', 'Me', 'Nd', 'Nl', 'No', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po', 'Sm', 'Sc', 'Sk', 'So', 'Zs', 'Zl', 'Zp', 'Cc', 'Cf', 'Cs', 'Co', 'Cn'];
    var GC_KO = { Lu: '대문자', Ll: '소문자', Lt: '타이틀케이스', Lm: '수정 문자', Lo: '기타 글자', Mn: '결합 표시(비간격)', Mc: '결합 표시(간격)', Me: '결합 표시(둘러싸기)', Nd: '십진 숫자', Nl: '글자형 숫자', No: '기타 숫자', Pc: '연결 구두점', Pd: '대시', Ps: '여는 괄호', Pe: '닫는 괄호', Pi: '여는 따옴표', Pf: '닫는 따옴표', Po: '기타 구두점', Sm: '수학 기호', Sc: '통화 기호', Sk: '수정 기호', So: '기타 기호', Zs: '공백', Zl: '줄 구분자', Zp: '문단 구분자', Cc: '제어 문자', Cf: '서식 문자', Cs: '대리 쌍 절반', Co: '사용자 정의', Cn: '미할당' };
    var GC_RE = GC.map(function (g) { return [g, new RegExp('^\\p{' + g + '}$', 'u')]; });
    var SCRIPTS = ['Latin', 'Greek', 'Cyrillic', 'Hangul', 'Han', 'Hiragana', 'Katakana', 'Arabic', 'Hebrew', 'Thai', 'Devanagari', 'Armenian', 'Georgian', 'Bengali', 'Tamil', 'Ethiopic', 'Khmer', 'Lao', 'Tibetan', 'Mongolian', 'Cherokee', 'Common', 'Inherited'];
    var SC_RE = SCRIPTS.map(function (s) { try { return [s, new RegExp('^\\p{Script=' + s + '}$', 'u')]; } catch (e) { return null; } }).filter(Boolean);
    function hex(n, w) { var s = n.toString(16).toUpperCase(); while (s.length < w) s = '0' + s; return s; }
    function utf8(cp) { return Array.prototype.map.call(new TextEncoder().encode(String.fromCodePoint(cp)), function (b) { return hex(b, 2); }).join(' '); }
    function nameOf(cp) {
      if (NAMES[cp]) return NAMES[cp];
      if (cp >= 0x41 && cp <= 0x5A) return 'LATIN CAPITAL LETTER ' + String.fromCharCode(cp);
      if (cp >= 0x61 && cp <= 0x7A) return 'LATIN SMALL LETTER ' + String.fromCharCode(cp - 32);
      if (cp >= 0x30 && cp <= 0x39) return 'DIGIT ' + ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE'][cp - 0x30];
      if (cp >= 0xAC00 && cp <= 0xD7A3) { var s = cp - 0xAC00; return 'HANGUL SYLLABLE ' + CHO[Math.floor(s / 588)] + JUNG[Math.floor((s % 588) / 28)] + JONG[s % 28]; }
      if ((cp >= 0x4E00 && cp <= 0x9FFF) || (cp >= 0x3400 && cp <= 0x4DBF) || (cp >= 0x20000 && cp <= 0x2A6DF)) return 'CJK UNIFIED IDEOGRAPH-' + hex(cp, 4);
      if (cp >= 0x1100 && cp <= 0x11FF) return 'HANGUL JAMO U+' + hex(cp, 4);
      if (cp >= 0x3131 && cp <= 0x318E) return 'HANGUL COMPATIBILITY JAMO U+' + hex(cp, 4);
      if (cp >= 0xFE00 && cp <= 0xFE0F) return 'VARIATION SELECTOR-' + (cp - 0xFE00 + 1);
      if (cp >= 0xE0100 && cp <= 0xE01EF) return 'VARIATION SELECTOR-' + (cp - 0xE0100 + 17);
      if (cp >= 0xE0020 && cp <= 0xE007E) return 'TAG ' + String.fromCharCode(cp - 0xE0000);
      if (cp >= 0xFF01 && cp <= 0xFF5E) return 'FULLWIDTH ' + (nameOf(cp - 0xFEE0).replace(/^LATIN /, ''));
      if (cp >= 0x1F300 && cp <= 0x1FAFF) return 'EMOJI / PICTOGRAPH U+' + hex(cp, 5);
      if (cp >= 0x80 && cp <= 0x9F) return 'C1 CONTROL U+' + hex(cp, 4);
      if (cp < 0x20) return 'C0 CONTROL U+' + hex(cp, 4);
      return '';
    }
    function vis(cp) {
      if (cp < 0x20) return String.fromCharCode(0x2400 + cp);
      if (cp === 0x7F) return '␡';
      if (cp === 0x20) return '␠';
      var gc = ''; for (var i = 0; i < GC_RE.length; i++) if (GC_RE[i][1].test(String.fromCodePoint(cp))) { gc = GC_RE[i][0]; break; }
      if (gc === 'Zs' || gc === 'Cf' || gc === 'Zl' || gc === 'Zp' || gc === 'Cc' || gc === 'Cn' || gc === 'Co' || gc === 'Cs') return '·';
      if (gc === 'Mn' || gc === 'Me' || gc === 'Mc') return '◌' + String.fromCodePoint(cp);
      return String.fromCodePoint(cp);
    }
    var cps = Array.from(text), rows = [], gcCount = {}, scCount = {}, lim = Number(o.limit) || 300, shown = 0, unit16 = text.length;
    cps.forEach(function (ch, idx) {
      var cp = ch.codePointAt(0), gc = '', sc = '';
      for (var i = 0; i < GC_RE.length; i++) if (GC_RE[i][1].test(ch)) { gc = GC_RE[i][0]; break; }
      for (var j = 0; j < SC_RE.length; j++) if (SC_RE[j][1].test(ch)) { sc = SC_RE[j][0]; break; }
      gcCount[gc] = (gcCount[gc] || 0) + 1; if (sc) scCount[sc] = (scCount[sc] || 0) + 1;
      if (o.hide && /^[A-Za-z0-9]$/.test(ch)) return;
      if (shown >= lim) return; shown++;
      var u16 = cp > 0xFFFF ? hex(ch.charCodeAt(0), 4) + ' ' + hex(ch.charCodeAt(1), 4) : hex(cp, 4);
      rows.push([String(idx + 1), vis(cp), 'U+' + hex(cp, 4), nameOf(cp) || '—', gc + ' ' + t(GC_KO[gc] || '', ''), sc || '—', utf8(cp), u16]);
    });
    var graphemes = null;
    if (typeof Intl !== 'undefined' && Intl.Segmenter) { graphemes = Array.from(new Intl.Segmenter(undefined, { granularity: 'grapheme' }).segment(text), function (s) { return s.segment; }); }
    var grRows = [];
    if (graphemes) graphemes.forEach(function (g, i) { if (i < 300 && Array.from(g).length > 1) grRows.push([String(i + 1), g, Array.from(g).map(function (c) { return 'U+' + hex(c.codePointAt(0), 4); }).join(' '), String(Array.from(g).length)]); });
    var forms = ['NFC', 'NFD', 'NFKC', 'NFKD'].filter(function (f) { return text.normalize(f) === text; });
    var bytes8 = new TextEncoder().encode(text).length;
    var info = [[['문자 수 (코드 포인트)', 'Code points'], String(cps.length)], [['문자소 수 (사용자가 보는 글자 수)', 'Grapheme clusters (user-perceived characters)'], graphemes ? String(graphemes.length) : '—'], [['UTF-16 코드 유닛 (JS length)', 'UTF-16 code units (JS length)'], String(unit16)], [['UTF-8 바이트', 'UTF-8 bytes'], String(bytes8)], [['이미 정규화된 형식', 'Already normalised as'], forms.length ? forms.join(', ') : t('없음 (NFC/NFD/NFKC/NFKD 모두 다름)', 'none')], [['스크립트', 'Scripts'], Object.keys(scCount).map(function (k) { return k + ' ' + scCount[k]; }).join(', ') || '—'], [['분류', 'Categories'], Object.keys(gcCount).map(function (k) { return k + ' ' + gcCount[k]; }).join(', ')]];
    var notes = [];
    if (cps.length > lim) notes.push('ℹ️ ' + t('표에는 처음 ' + lim + '개 코드 포인트만 표시합니다', 'The table lists the first ' + lim + ' code points only'));
    if (graphemes && graphemes.length !== cps.length) notes.push('ℹ️ ' + t('코드 포인트 ' + cps.length + '개가 화면에서는 ' + graphemes.length + '글자로 보입니다 (결합 문자·이모지 조합). length 로 글자 수를 세면 틀립니다', cps.length + ' code points appear as ' + graphemes.length + ' characters (combining marks / emoji sequences); counting with length would be wrong'));
    if (text.length !== cps.length) notes.push('ℹ️ ' + t('BMP 밖의 문자(이모지 등)는 UTF-16 에서 코드 유닛 2개를 차지해 JS 의 length 가 더 큽니다', 'Characters outside the BMP (emoji etc.) take two UTF-16 units, so JS length is larger'));
    if (cps.some(function (c) { var n = c.codePointAt(0); return (n >= 0x200B && n <= 0x200F) || (n >= 0x202A && n <= 0x202E) || (n >= 0x2060 && n <= 0x2064) || n === 0xFEFF || n === 0xAD || (n >= 0x2066 && n <= 0x2069); })) notes.push('⚠️ ' + t('눈에 보이지 않는 서식 문자(제로폭·방향 제어 등)가 있습니다. "보이지 않는 문자 탐지기"로 자세히 확인하세요', 'Invisible format characters (zero-width, bidi controls ...) are present; check them with the invisible character detector'));
    if (/[ᄀ-ᇿ㄰-㆏]/.test(text) && /[ᅡ-ᇂ]/.test(text)) notes.push('ℹ️ ' + t('한글 자모가 분리된 형태(NFD)가 섞여 있습니다. macOS 파일명처럼 NFC 와 NFD 가 다르면 검색·비교가 실패할 수 있습니다', 'Decomposed Hangul jamo (NFD) are present; differences between NFC and NFD (e.g. macOS file names) can break search and comparison'));
    notes.push('ℹ️ ' + t('문자 이름은 자주 쓰는 문자·한글 음절·CJK 한자만 제공합니다. 분류와 스크립트는 모든 문자에 대해 브라우저의 유니코드 데이터로 판별합니다', 'Names are provided for common characters, Hangul syllables and CJK ideographs; category and script come from the browser\'s Unicode data for every character'));
    return { _status: t('✅ 코드 포인트 ' + cps.length + '개 · 문자소 ' + (graphemes ? graphemes.length : '?') + '개 · UTF-8 ' + bytes8 + '바이트', '✅ ' + cps.length + ' code points · ' + (graphemes ? graphemes.length : '?') + ' graphemes · ' + bytes8 + ' UTF-8 bytes'), info: info, table: { head: [['#', '#'], ['글자', 'Char'], ['코드 포인트', 'Code point'], ['이름', 'Name'], ['분류', 'Category'], ['스크립트', 'Script'], ['UTF-8', 'UTF-8'], ['UTF-16', 'UTF-16']], rows: rows }, gr: { head: [['#', '#'], ['문자소', 'Grapheme'], ['구성 코드 포인트', 'Code points'], ['개수', 'Count']], rows: grRows, empty: ['여러 코드 포인트로 이루어진 문자소가 없습니다', 'No multi-code-point graphemes'] }, issues: notes };
  }
});
