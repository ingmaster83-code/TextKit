TK.tool('icu-message-tester', {
  sampleExpectError: false,
  inputs: [
    { id: 'in', label: ['ICU 메시지 (MessageFormat)', 'ICU message (MessageFormat)'], rows: 6, sample: '{gender, select, female{그녀는} male{그는} other{그들은}} 사진 {count, plural, =0{없음} =1{한 장을} other{# 장을}} 올렸습니다. 총액 {price, number, ::currency/KRW}, {when, date, long}' },
    { id: 'args', label: ['인자 값 (JSON 객체)', 'Argument values (JSON object)'], rows: 5, sample: '{"gender":"female","count":3,"price":12500,"when":"2026-10-17T09:00:00Z"}' }
  ],
  options: [
    { id: 'loc', type: 'text', label: ['로케일', 'Locale'], default: 'ko-KR', placeholder: ['예: en-US, ru, ar-EG', 'e.g. en-US, ru, ar-EG'] },
    { id: 'tz', type: 'text', label: ['시간대 (날짜 서식)', 'Time zone (dates)'], default: 'UTC' }
  ],
  sampleOptions: { loc: 'ko-KR' },
  outputs: [{ id: 'out', label: ['서식 결과', 'Formatted result'], kind: 'code', ext: 'txt' }, { id: 'table', label: ['인자', 'Arguments'], kind: 'table' }, { id: 'ast', label: ['구문 트리 (JSON)', 'Parsed AST (JSON)'], kind: 'code', ext: 'json' }, { id: 'issues', label: ['점검 결과', 'Findings'], kind: 'list' }],
  run: function (v, o, t) {
    var src = String(v['in'] == null ? '' : v['in']); if (!src.trim()) throw new Error(t('ICU 메시지를 입력하세요', 'Enter an ICU message'));
    var args = {}, argText = String(v.args == null ? '' : v.args).trim();
    if (argText) { try { args = JSON.parse(argText); } catch (e) { throw new Error(t('인자 JSON 구문 오류: ', 'Arguments JSON syntax error: ') + e.message); } if (!args || typeof args !== 'object' || Array.isArray(args)) throw new Error(t('인자는 JSON 객체여야 합니다', 'Arguments must be a JSON object')); }
    var locale = String(o.loc || 'en-US').trim().replace(/_/g, '-'), loc;
    try { loc = new Intl.Locale(locale).toString(); } catch (e) { throw new Error(t('로케일이 올바르지 않습니다: ', 'Invalid locale: ') + locale); }
    var issues = [], used = {}, types = {};
    function err(msg, pos) { var e = new Error(msg); e.pos = pos; throw e; }
    /* ---------------- 파서 ---------------- */
    var pos = 0, n = src.length;
    function parseElements(inPlural, depth, stopAtBrace) {
      var out = [], buf = '';
      function flush() { if (buf) { out.push({ type: 'text', value: buf }); buf = ''; } }
      while (pos < n) {
        var c = src[pos];
        if (c === "'") {
          if (src[pos + 1] === "'") { buf += "'"; pos += 2; continue; }
          var nx = src[pos + 1];
          if (nx === '{' || nx === '}' || (inPlural && nx === '#') || (depth > 0 && nx === '|')) {
            pos++; /* 따옴표 구간 시작 */
            while (pos < n) { if (src[pos] === "'") { if (src[pos + 1] === "'") { buf += "'"; pos += 2; continue; } pos++; break; } buf += src[pos++]; }
            continue;
          }
          buf += c; pos++; continue;
        }
        if (c === '{') { flush(); out.push(parseArg(inPlural, depth)); continue; }
        if (c === '}') { if (stopAtBrace) break; err(t('짝이 없는 } 입니다 (위치 ' + pos + ')', 'Unmatched } (position ' + pos + ')'), pos); }
        if (c === '#' && inPlural) { flush(); out.push({ type: 'pound' }); pos++; continue; }
        buf += c; pos++;
      }
      flush();
      return out;
    }
    function skipWs() { while (pos < n && /\s/.test(src[pos])) pos++; }
    function readId() { var m = /^[^\s{},#'"]+/.exec(src.slice(pos)); if (!m) err(t('인자 이름이 필요합니다 (위치 ' + pos + ')', 'Argument name expected (position ' + pos + ')'), pos); pos += m[0].length; return m[0]; }
    function parseArg(inPlural, depth) {
      var start = pos; pos++; skipWs();
      var name = readId(); skipWs();
      if (src[pos] === '}') { pos++; used[name] = true; types[name] = types[name] || 'any'; return { type: 'arg', name: name }; }
      if (src[pos] !== ',') err(t('"," 또는 "}" 가 필요합니다 (위치 ' + pos + ')', 'Expected "," or "}" (position ' + pos + ')'), pos);
      pos++; skipWs();
      var kind = readId(); skipWs(); used[name] = true;
      if (kind === 'number' || kind === 'date' || kind === 'time') {
        var style = '';
        if (src[pos] === ',') { pos++; skipWs(); var st = ''; while (pos < n && src[pos] !== '}') { if (src[pos] === "'") { pos++; while (pos < n && src[pos] !== "'") st += src[pos++]; pos++; continue; } st += src[pos++]; } style = st.trim(); }
        if (src[pos] !== '}') err(t('} 가 필요합니다 (위치 ' + pos + ')', 'Expected } (position ' + pos + ')'), pos);
        pos++; types[name] = kind; return { type: kind, name: name, style: style };
      }
      if (kind === 'plural' || kind === 'selectordinal' || kind === 'select') {
        if (src[pos] !== ',') err(t(kind + ' 뒤에 "," 가 필요합니다 (위치 ' + pos + ')', 'Expected "," after ' + kind + ' (position ' + pos + ')'), pos);
        pos++; skipWs();
        var offset = 0, om = /^offset\s*:\s*(-?\d+)/.exec(src.slice(pos));
        if (kind !== 'select' && om) { offset = +om[1]; pos += om[0].length; skipWs(); }
        var options = {}, order = [];
        while (pos < n && src[pos] !== '}') {
          var key = ''; if (src[pos] === '=') { pos++; var km = /^-?\d+(?:\.\d+)?/.exec(src.slice(pos)); if (!km) err(t('= 뒤에 숫자가 필요합니다 (위치 ' + pos + ')', 'A number is expected after = (position ' + pos + ')'), pos); key = '=' + km[0]; pos += km[0].length; } else key = readId();
          skipWs();
          if (src[pos] !== '{') err(t('"' + key + '" 뒤에 { 가 필요합니다 (위치 ' + pos + ')', 'Expected { after "' + key + '" (position ' + pos + ')'), pos);
          pos++;
          if (options[key]) issues.push('⛔ ' + t('"' + name + '" 에 "' + key + '" 옵션이 두 번 있습니다', '"' + name + '" has the option "' + key + '" twice'));
          options[key] = parseElements(kind !== 'select', depth + 1, true); order.push(key);
          if (src[pos] !== '}') err(t('"' + key + '" 옵션의 } 가 없습니다', 'Missing } for the "' + key + '" option'), pos);
          pos++; skipWs();
        }
        if (src[pos] !== '}') err(t('"' + name + '" 의 } 가 없습니다 (' + kind + ' 가 닫히지 않음)', 'Missing } for "' + name + '" (' + kind + ' is not closed)'), pos);
        pos++; types[name] = kind;
        return { type: kind, name: name, offset: offset, options: options, order: order };
      }
      err(t('알 수 없는 인자 종류 "' + kind + '" (number, date, time, plural, selectordinal, select 중 하나)', 'Unknown argument type "' + kind + '" (number, date, time, plural, selectordinal or select)'), pos);
    }
    var ast;
    try { ast = parseElements(false, 0, false); } catch (e) {
      var ctx = src.slice(Math.max(0, (e.pos || 0) - 15), (e.pos || 0) + 15).replace(/\n/g, '↵');
      throw new Error(t('구문 오류: ', 'Syntax error: ') + e.message + (e.pos !== undefined ? '  … ' + ctx + ' …' : ''));
    }
    /* ---------------- 검사 + 포매팅 ---------------- */
    var pr, prOrd, cats, catsOrd;
    try { pr = new Intl.PluralRules(loc); cats = pr.resolvedOptions().pluralCategories; prOrd = new Intl.PluralRules(loc, { type: 'ordinal' }); catsOrd = prOrd.resolvedOptions().pluralCategories; } catch (e) { cats = ['other']; catsOrd = ['other']; }
    var tz = String(o.tz || 'UTC').trim() || 'UTC';
    try { new Intl.DateTimeFormat(loc, { timeZone: tz }); } catch (e) { throw new Error(t('시간대가 올바르지 않습니다: ', 'Invalid time zone: ') + tz); }
    var missing = {};
    function numOpts(style) {
      var s = (style || '').trim();
      if (!s) return {};
      if (s === 'integer') return { maximumFractionDigits: 0 };
      if (s === 'percent') return { style: 'percent' };
      if (s === 'currency') return { style: 'currency', currency: 'USD' };
      if (s.indexOf('::') === 0) {
        var op = {}, toks = s.slice(2).split(/\s+/);
        toks.forEach(function (tk) {
          var m;
          if ((m = /^currency\/([A-Za-z]{3})$/.exec(tk))) { op.style = 'currency'; op.currency = m[1].toUpperCase(); }
          else if (tk === 'percent') op.style = 'percent';
          else if (tk === 'compact-short') { op.notation = 'compact'; op.compactDisplay = 'short'; }
          else if (tk === 'compact-long') { op.notation = 'compact'; op.compactDisplay = 'long'; }
          else if (tk === 'scientific') op.notation = 'scientific';
          else if ((m = /^unit\/([a-z-]+)$/.exec(tk))) { op.style = 'unit'; op.unit = m[1]; }
          else if ((m = /^\.(0*)(#*)$/.exec(tk))) { op.minimumFractionDigits = m[1].length; op.maximumFractionDigits = m[1].length + m[2].length; }
          else if (tk === 'integer-width/*000') { }
          else if (tk === 'sign-always') op.signDisplay = 'always';
          else if (tk === 'group-off') op.useGrouping = false;
          else if (tk === 'precision-integer') op.maximumFractionDigits = 0;
          else issues.push('⚠️ ' + t('number 스켈레톤 "' + tk + '" 은(는) 지원하지 않아 무시했습니다', 'The number skeleton "' + tk + '" is not supported and was ignored'));
        });
        return op;
      }
      issues.push('⚠️ ' + t('number 스타일 "' + s + '" 을(를) 알 수 없습니다 (integer, percent, currency 또는 ::스켈레톤)', 'Unknown number style "' + s + '" (integer, percent, currency or ::skeleton)'));
      return {};
    }
    function dateOpts(kind, style) {
      var s = (style || 'medium').trim() || 'medium';
      if (['short', 'medium', 'long', 'full'].indexOf(s) >= 0) { var o2 = {}; if (kind === 'date') o2.dateStyle = s; else o2.timeStyle = s; o2.timeZone = tz; return o2; }
      if (s.indexOf('::') === 0) {
        var sk = s.slice(2), op = { timeZone: tz }, m;
        if (/y{4}/.test(sk)) op.year = 'numeric'; else if (/yy/.test(sk)) op.year = '2-digit'; else if (/y/.test(sk)) op.year = 'numeric';
        if (/M{5}/.test(sk)) op.month = 'narrow'; else if (/M{4}/.test(sk)) op.month = 'long'; else if (/M{3}/.test(sk)) op.month = 'short'; else if (/MM/.test(sk)) op.month = '2-digit'; else if (/M/.test(sk)) op.month = 'numeric';
        if (/dd/.test(sk)) op.day = '2-digit'; else if (/d/.test(sk)) op.day = 'numeric';
        if (/E{4}/.test(sk)) op.weekday = 'long'; else if (/E/.test(sk)) op.weekday = 'short';
        if (/H/.test(sk)) { op.hour = /HH/.test(sk) ? '2-digit' : 'numeric'; op.hour12 = false; } else if (/h/.test(sk)) { op.hour = /hh/.test(sk) ? '2-digit' : 'numeric'; op.hour12 = true; }
        if (/m/.test(sk)) op.minute = '2-digit'; if (/s/.test(sk)) op.second = '2-digit';
        if (/z/.test(sk)) op.timeZoneName = 'short';
        return op;
      }
      issues.push('⚠️ ' + t(kind + ' 스타일 "' + s + '" 을(를) 알 수 없습니다 (short, medium, long, full 또는 ::스켈레톤)', 'Unknown ' + kind + ' style "' + s + '" (short, medium, long, full or ::skeleton)'));
      return { dateStyle: 'medium', timeZone: tz };
    }
    function fmt(elements, pound, poundSrc) {
      var out = '';
      elements.forEach(function (el) {
        switch (el.type) {
          case 'text': out += el.value; break;
          case 'pound': out += pound === undefined ? '#' : pound; break;
          case 'arg': { if (!(el.name in args)) { missing[el.name] = 1; out += '{' + el.name + '}'; } else out += typeof args[el.name] === 'object' ? JSON.stringify(args[el.name]) : String(args[el.name]); break; }
          case 'number': { if (!(el.name in args)) { missing[el.name] = 1; out += '{' + el.name + '}'; break; } var nv = Number(args[el.name]); if (isNaN(nv)) { issues.push('⛔ ' + t('"' + el.name + '" 은(는) 숫자여야 합니다 (값: ' + JSON.stringify(args[el.name]) + ')', '"' + el.name + '" must be a number (value: ' + JSON.stringify(args[el.name]) + ')')); out += '{' + el.name + '}'; break; } try { out += new Intl.NumberFormat(loc, numOpts(el.style)).format(nv); } catch (e) { issues.push('⛔ ' + t('숫자 서식 오류: ', 'Number format error: ') + e.message); out += String(nv); } break; }
          case 'date': case 'time': { if (!(el.name in args)) { missing[el.name] = 1; out += '{' + el.name + '}'; break; } var dv = new Date(typeof args[el.name] === 'number' ? args[el.name] : String(args[el.name])); if (isNaN(dv)) { issues.push('⛔ ' + t('"' + el.name + '" 은(는) 날짜로 해석할 수 없습니다 (ISO 문자열이나 밀리초를 사용하세요)', '"' + el.name + '" is not a valid date (use an ISO string or milliseconds)')); out += '{' + el.name + '}'; break; } try { out += new Intl.DateTimeFormat(loc, dateOpts(el.type, el.style)).format(dv); } catch (e) { issues.push('⛔ ' + t('날짜 서식 오류: ', 'Date format error: ') + e.message); } break; }
          case 'select': { if (!(el.name in args)) { missing[el.name] = 1; out += '{' + el.name + '}'; break; } var key = String(args[el.name]), opt = el.options[key] || el.options.other; if (!el.options.other) issues.push('⛔ ' + t('select "' + el.name + '" 에 필수 옵션 other 가 없습니다', 'select "' + el.name + '" has no required "other" option')); if (!opt) { out += '{' + el.name + '}'; break; } out += fmt(opt, pound); break; }
          case 'plural': case 'selectordinal': {
            if (!(el.name in args)) { missing[el.name] = 1; out += '{' + el.name + '}'; break; }
            var val = Number(args[el.name]);
            if (isNaN(val)) { issues.push('⛔ ' + t('"' + el.name + '" 은(는) 숫자여야 합니다 (값: ' + JSON.stringify(args[el.name]) + ')', '"' + el.name + '" must be a number (value: ' + JSON.stringify(args[el.name]) + ')')); out += '{' + el.name + '}'; break; }
            if (!el.options.other) issues.push('⛔ ' + t(el.type + ' "' + el.name + '" 에 필수 옵션 other 가 없습니다', el.type + ' "' + el.name + '" has no required "other" option'));
            var adj = val - (el.offset || 0), exact = el.options['=' + val], pick = exact, shown;
            if (!pick) { var cat = (el.type === 'plural' ? pr : prOrd).select(adj); pick = el.options[cat] || el.options.other; shown = cat; }
            if (!pick) { out += '{' + el.name + '}'; break; }
            out += fmt(pick, new Intl.NumberFormat(loc).format(adj));
            break;
          }
        }
      });
      return out;
    }
    var result = fmt(ast, undefined);
    /* 정적 검사 */
    (function check(els, parentPlural) {
      els.forEach(function (el) {
        if (el.type === 'pound' && !parentPlural) issues.push('ℹ️ ' + t('plural 밖의 # 는 그냥 문자입니다 (따옴표로 감싸지 않아도 됩니다)', '# outside a plural is plain text'));
        if (el.type === 'plural' || el.type === 'selectordinal') {
          var allowed = (el.type === 'plural' ? cats : catsOrd).concat([]);
          el.order.forEach(function (k) { if (!/^=/.test(k) && ['zero', 'one', 'two', 'few', 'many', 'other'].indexOf(k) < 0) issues.push('⛔ ' + t('"' + k + '" 는 올바른 plural 범주가 아닙니다 (zero, one, two, few, many, other 또는 =숫자)', '"' + k + '" is not a plural category (zero, one, two, few, many, other or =number)')); else if (!/^=/.test(k) && allowed.indexOf(k) < 0) issues.push('⚠️ ' + t(loc + ' 에서는 "' + k + '" 범주를 쓰지 않습니다. 사용하는 범주: ' + allowed.join(', '), 'Locale ' + loc + ' does not use the "' + k + '" category; it uses: ' + allowed.join(', '))); });
          var missingCat = allowed.filter(function (c) { return el.order.indexOf(c) < 0 && c !== 'other' && !(el.order.indexOf('=' + (c === 'zero' ? 0 : c === 'one' ? 1 : c === 'two' ? 2 : -999)) >= 0); });
          if (missingCat.length && el.type === 'plural') issues.push('⚠️ ' + t('"' + el.name + '" 에 ' + loc + ' 의 범주 ' + missingCat.join(', ') + ' 가 없어 해당 숫자는 other 로 표시됩니다', '"' + el.name + '" lacks the ' + loc + ' categories ' + missingCat.join(', ') + '; those numbers fall back to other'));
          if (missingCat.length && el.type === 'selectordinal') issues.push('ℹ️ ' + t('"' + el.name + '" 서수에 ' + loc + ' 의 범주 ' + missingCat.join(', ') + ' 가 없습니다', 'The ordinal "' + el.name + '" lacks the ' + loc + ' categories ' + missingCat.join(', ')));
          el.order.forEach(function (k) { check(el.options[k], true); });
        } else if (el.type === 'select') { if (!el.options.other) { } el.order.forEach(function (k) { check(el.options[k], parentPlural); }); }
      });
    })(ast, false);
    var argNames = Object.keys(types), rows = argNames.map(function (nm) {
      var has = nm in args, val = has ? JSON.stringify(args[nm]) : '—';
      return [nm, types[nm] === 'any' ? t('단순 치환', 'simple') : types[nm], val, has ? '✅' : '⛔ ' + t('값 없음', 'missing')];
    });
    Object.keys(missing).forEach(function (m) { issues.push('⛔ ' + t('인자 "' + m + '" 의 값이 없어 {' + m + '} 그대로 출력됩니다', 'No value for argument "' + m + '", so {' + m + '} is printed as is')); });
    Object.keys(args).forEach(function (k) { if (!types[k]) issues.push('ℹ️ ' + t('값 "' + k + '" 은(는) 메시지에서 쓰이지 않습니다', 'The value "' + k + '" is not used by the message')); });
    issues.push('ℹ️ ' + t('로케일 ' + loc + ' 의 plural 범주: ' + cats.join(', ') + ' | 서수: ' + catsOrd.join(', '), 'Plural categories for ' + loc + ': ' + cats.join(', ') + ' | ordinal: ' + catsOrd.join(', ')));
    var errCount = issues.filter(function (s) { return s.indexOf('⛔') === 0; }).length;
    function strip(els) { return els.map(function (el) { if (el.options) { var o2 = {}; el.order.forEach(function (k) { o2[k] = strip(el.options[k]); }); return { type: el.type, name: el.name, offset: el.offset || undefined, options: o2 }; } return el; }); }
    return { _status: errCount ? { ok: false, msg: t('⛔ 문제 ' + errCount + '건', '⛔ ' + errCount + ' problem(s)') } : t('✅ 서식 성공 (' + loc + ')', '✅ Formatted (' + loc + ')'), out: result, table: { head: [['인자', 'Argument'], ['종류', 'Type'], ['입력 값', 'Value'], ['상태', 'Status']], rows: rows, empty: ['인자가 없는 메시지입니다', 'The message has no arguments'] }, ast: JSON.stringify(strip(ast), null, 2), issues: issues };
  }
});
