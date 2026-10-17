TK.tool('text-pattern-extractor', {
  inputs: [{ id: 'in', label: ['텍스트', 'Text'], rows: 10, sample: '문의: help@wooahouse.com, sales@example.co.kr / 전화 02-1234-5678, 010-9876-5432\n서버 192.168.0.10 (백업 10.0.0.255) 접속 https://wooahouse.com/docs?id=7, http://example.org/a.\n결제 금액 1,250,000원, 주문번호 3f2504e0-4f89-41d3-9a0c-0305e82c3301, 색상 #ff6600\n태그 #우아하우스 #devtools 담당 @wooa_dev 마감 2026-10-17 (2026년 11월 3일)' }],
  options: [
    { id: 'type', type: 'select', label: ['추출할 항목', 'What to extract'], choices: [['all', ['모두 (유형별 개수 요약)', 'All types (count summary)']], ['email', ['이메일', 'Email addresses']], ['url', 'URL'], ['phone-kr', ['전화번호 (한국)', 'Phone numbers (Korea)']], ['phone-intl', ['전화번호 (국제 +CC)', 'Phone numbers (international)']], ['ipv4', 'IPv4'], ['ipv6', 'IPv6'], ['date', ['날짜', 'Dates']], ['money', ['금액 (원·₩)', 'Amounts (KRW)']], ['number', ['숫자', 'Numbers']], ['hashtag', ['해시태그', 'Hashtags']], ['mention', ['@멘션', '@mentions']], ['hex-color', ['16진수 색상', 'Hex colours']], ['uuid', 'UUID'], ['rrn', ['주민등록번호 형식', 'Korean RRN format']], ['card', ['카드번호 (Luhn 검사)', 'Card numbers (Luhn)']], ['korean', ['한글 단어', 'Korean words']], ['english', ['영어 단어', 'English words']], ['custom', ['직접 입력한 정규식', 'Custom regex']]], default: 'all' },
    { id: 'regex', type: 'text', label: ['정규식 (직접 입력 선택 시)', 'Regex (for Custom)'], default: '', placeholder: ['예: \\b[A-Z]{2,}\\d+\\b', 'e.g. \\b[A-Z]{2,}\\d+\\b'], show: function (o) { return o.type === 'custom'; } },
    { id: 'flags', type: 'text', label: ['정규식 플래그 (i m s u)', 'Regex flags (i m s u)'], default: 'u', show: function (o) { return o.type === 'custom'; } },
    { id: 'uniq', type: 'checkbox', label: ['중복 제거', 'Remove duplicates'], default: true },
    { id: 'sort', type: 'select', label: ['정렬', 'Sort'], choices: [['pos', ['등장 순서', 'Order of appearance']], ['alpha', ['가나다·ABC 순', 'Alphabetical']], ['count', ['많이 나온 순', 'Most frequent first']]], default: 'pos' }
  ],
  outputs: [{ id: 'sum', label: ['유형별 개수', 'Counts by type'], kind: 'table' }, { id: 'table', label: ['추출 결과', 'Matches'], kind: 'table' }, { id: 'out', label: ['한 줄에 하나씩', 'One per line'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var text = String(v['in'] || ''); if (!text.trim()) throw new Error(t('텍스트를 입력하세요', 'Enter some text'));
    var notes = [];
    function luhn(s) { var d = s.replace(/\D/g, ''); if (d.length < 13 || d.length > 19) return false; var sum = 0, alt = false; for (var i = d.length - 1; i >= 0; i--) { var n = +d[i]; if (alt) { n *= 2; if (n > 9) n -= 9; } sum += n; alt = !alt; } return sum % 10 === 0; }
    var P = {
      email: { re: /[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}/g },
      url: { re: /https?:\/\/[^\s<>"'`]+/gi, fix: function (s) { return s.replace(/[.,;:!?)\]}'"]+$/, ''); } },
      'phone-kr': { re: /(?:\+82[\s-]?|\b)0?(?:2|[3-6]\d|1[016789]|70|80)[\s.-]?\d{3,4}[\s.-]?\d{4}\b/g, ok: function (s) { return /\d{9,11}/.test(s.replace(/\D/g, '')); } },
      'phone-intl': { re: /\+\d{1,3}[\s.-]?\(?\d{1,4}\)?(?:[\s.-]?\d{2,4}){2,4}/g },
      ipv4: { re: /\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b/g },
      ipv6: { re: /(?<![\w:])(?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:))(?![\w:])/g },
      date: { re: /\b\d{4}[-./]\d{1,2}[-./]\d{1,2}\b|\d{4}\s*년\s*\d{1,2}\s*월\s*\d{1,2}\s*일/g },
      money: { re: /₩\s*\d[\d,]*|\d[\d,]*(?:\.\d+)?\s*(?:억|만)?\s*원/g },
      number: { re: /[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|[-+]?\d+(?:\.\d+)?/g },
      hashtag: { re: /#[\p{L}\p{N}_]+/gu, ok: function (s) { return !/^#[0-9a-fA-F]{3,8}$/.test(s) || /[g-zG-Z_]/.test(s); } },
      mention: { re: /(?<![\w.])@[A-Za-z0-9_]{1,30}\b/g },
      'hex-color': { re: /#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b/g },
      uuid: { re: /\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b/g },
      rrn: { re: /\b\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])-?[1-8]\d{6}\b/g },
      card: { re: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{1,7}\b/g, ok: luhn },
      korean: { re: /[가-힣]+/g },
      english: { re: /[A-Za-z]+(?:'[A-Za-z]+)?/g }
    };
    var LABEL = { email: t('이메일', 'Email'), url: 'URL', 'phone-kr': t('전화(한국)', 'Phone (KR)'), 'phone-intl': t('전화(국제)', 'Phone (intl)'), ipv4: 'IPv4', ipv6: 'IPv6', date: t('날짜', 'Date'), money: t('금액', 'Amount'), number: t('숫자', 'Number'), hashtag: t('해시태그', 'Hashtag'), mention: '@' + t('멘션', 'mention'), 'hex-color': t('색상', 'Colour'), uuid: 'UUID', rrn: t('주민번호 형식', 'RRN format'), card: t('카드번호', 'Card'), korean: t('한글 단어', 'Korean word'), english: t('영어 단어', 'English word') };
    function run1(key, def) {
      var out = [], m, re = new RegExp(def.re.source, def.re.flags.indexOf('g') >= 0 ? def.re.flags : def.re.flags + 'g');
      while ((m = re.exec(text))) {
        var s = def.fix ? def.fix(m[0]) : m[0];
        if (m[0] === '') { re.lastIndex++; continue; }
        if (def.ok && !def.ok(s)) continue;
        out.push({ v: s.trim(), pos: m.index, type: key });
      }
      return out;
    }
    var rows = [], sum = [];
    if (o.type === 'all') {
      ['email', 'url', 'phone-kr', 'phone-intl', 'ipv4', 'ipv6', 'date', 'money', 'hashtag', 'mention', 'hex-color', 'uuid', 'rrn', 'card'].forEach(function (k) {
        var r = run1(k, P[k]); if (k === 'phone-intl') r = r.filter(function (x) { return !rows.some(function (y) { return y.type === 'phone-kr' && text.indexOf(y.v) === x.pos; }); });
        rows = rows.concat(r); sum.push([LABEL[k], String(r.length), String(new Set(r.map(function (x) { return x.v; })).size)]);
      });
      /* 서로 겹치는 항목(예: URL 안의 숫자)은 유형별 개수에서만 중복 계산 */
    } else if (o.type === 'custom') {
      var src = String(o.regex || ''); if (!src) throw new Error(t('정규식을 입력하세요', 'Enter a regular expression'));
      var fl = String(o.flags || '').replace(/[^imsu]/g, '');
      var re2; try { re2 = new RegExp(src, fl + 'g'); } catch (e) { throw new Error(t('정규식 오류: ', 'Invalid regex: ') + e.message); }
      var mm, guard = 0;
      while ((mm = re2.exec(text)) && guard++ < 100000) { if (mm[0] === '') { re2.lastIndex++; continue; } rows.push({ v: mm[0], pos: mm.index, type: 'custom', groups: mm.slice(1) }); }
      sum.push([t('정규식', 'Regex'), String(rows.length), String(new Set(rows.map(function (x) { return x.v; })).size)]);
    } else {
      rows = run1(o.type, P[o.type]);
      sum.push([LABEL[o.type], String(rows.length), String(new Set(rows.map(function (x) { return x.v; })).size)]);
    }
    /* 위치 → 줄:열 */
    var lineStarts = [0]; for (var i = 0; i < text.length; i++) if (text[i] === '\n') lineStarts.push(i + 1);
    function lc(pos) { var lo = 0, hi = lineStarts.length - 1; while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (lineStarts[mid] <= pos) lo = mid; else hi = mid - 1; } return (lo + 1) + ':' + (pos - lineStarts[lo] + 1); }
    var agg = {}, order = [];
    rows.forEach(function (r) { var key = r.type + '\u0000' + r.v; if (!agg[key]) { agg[key] = { v: r.v, type: r.type, count: 0, pos: r.pos }; order.push(key); } agg[key].count++; });
    var list = o.uniq ? order.map(function (k) { return agg[k]; }) : rows.map(function (r) { return { v: r.v, type: r.type, count: 1, pos: r.pos }; });
    if (o.sort === 'alpha') list.sort(function (a, b) { return a.v < b.v ? -1 : a.v > b.v ? 1 : 0; });
    else if (o.sort === 'count') list.sort(function (a, b) { return b.count - a.count || a.pos - b.pos; });
    else list.sort(function (a, b) { return a.pos - b.pos; });
    var table = list.slice(0, 3000).map(function (x) { return [x.v, o.type === 'all' ? LABEL[x.type] : '', String(x.count), lc(x.pos)]; });
    if (o.type !== 'all') table = table.map(function (r) { return [r[0], r[2], r[3]]; });
    var head = o.type === 'all' ? [['값', 'Value'], ['유형', 'Type'], ['횟수', 'Count'], ['처음 위치(줄:열)', 'First (line:col)']] : [['값', 'Value'], ['횟수', 'Count'], ['처음 위치(줄:열)', 'First (line:col)']];
    if (list.length > 3000) notes.push(t('표에는 처음 3,000개만 표시합니다', 'The table shows the first 3,000 matches only'));
    if (rows.some(function (r) { return r.type === 'rrn'; })) notes.push('⚠️ ' + t('주민등록번호 형식으로 보이는 값이 있습니다. 개인정보이므로 공유·저장에 주의하세요', 'Values that look like Korean resident registration numbers were found; they are personal data, so be careful when sharing or storing them'));
    if (rows.some(function (r) { return r.type === 'card'; })) notes.push('⚠️ ' + t('Luhn 검사를 통과한 카드번호 형식이 있습니다. 결제 정보이므로 노출에 주의하세요', 'Values passing the Luhn check were found; treat them as payment data'));
    if (o.type === 'all') notes.push('ℹ️ ' + t('"모두" 모드는 유형마다 따로 찾으므로 URL 안의 IP·날짜처럼 같은 글자가 여러 유형에 잡힐 수 있습니다', '"All" runs each type separately, so the same characters (e.g. an IP inside a URL) can be counted under several types'));
    if (o.type === 'phone-kr' || o.type === 'all') notes.push('ℹ️ ' + t('전화번호는 형식만 보고 찾으며 실제 사용 가능한 번호인지는 확인하지 않습니다', 'Phone numbers are matched by format only; they are not verified'));
    if (!rows.length) notes.push('ℹ️ ' + t('일치하는 항목이 없습니다', 'No matches found'));
    return { _status: rows.length ? t('✅ ' + rows.length + '개 찾음' + (o.uniq ? ' (고유 ' + order.length + '개)' : ''), '✅ ' + rows.length + ' match(es)' + (o.uniq ? ' (' + order.length + ' unique)' : '')) : { ok: 'info', msg: t('일치하는 항목이 없습니다', 'No matches') }, sum: { head: [['유형', 'Type'], ['전체', 'Total'], ['고유', 'Unique']], rows: sum }, table: { head: head, rows: table, empty: ['일치하는 항목이 없습니다', 'No matches'] }, out: list.map(function (x) { return x.v; }).join('\n'), issues: notes };
  }
});
