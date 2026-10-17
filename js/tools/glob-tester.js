TK.tool('glob-tester', {
  inputs: [
    { id: 'pat', label: ['패턴 (한 줄에 하나, # 주석, ! 로 시작하면 제외)', 'Patterns (one per line, # comments, a leading ! excludes)'], rows: 6, sample: 'src/**/*.{js,ts}\n!**/*.test.*\n*.md\n# 숨김 파일은 기본적으로 제외됩니다\n**/node_modules/**' },
    { id: 'in', label: ['경로 목록 (한 줄에 하나)', 'Paths (one per line)'], rows: 10, sample: 'src/index.js\nsrc/utils/format.ts\nsrc/utils/format.test.ts\nsrc/.hidden/config.js\nREADME.md\ndocs/guide.md\nnode_modules/lib/index.js\npackage.json\nlib/a/b/c.js' }
  ],
  options: [
    { id: 'mode', type: 'select', label: ['규칙', 'Rules'], choices: [['glob', ['glob (minimatch 방식: 하나라도 일치하면 포함, ! 는 제외)', 'glob (minimatch style: any match includes, ! excludes)']], ['gitignore', ['.gitignore (마지막으로 일치한 규칙이 우선)', '.gitignore (last matching rule wins)']]], default: 'glob' },
    { id: 'dot', type: 'checkbox', label: ['점(.)으로 시작하는 파일·폴더도 * 와 ** 에 일치 (glob)', 'Let * and ** match dotfiles (glob)'], default: false },
    { id: 'nocase', type: 'checkbox', label: ['대소문자 구분 안 함', 'Case-insensitive'], default: false }
  ],
  outputs: [{ id: 'res', label: ['경로별 결과', 'Result per path'], kind: 'table' }, { id: 'rx', label: ['패턴 → 정규식', 'Pattern → regex'], kind: 'table' }, { id: 'out', label: ['일치한 경로', 'Matched paths'], kind: 'code', ext: 'txt' }, { id: 'issues', label: ['참고', 'Notes'], kind: 'list' }],
  run: function (v, o, t) {
    var rawPats = String(v.pat || '').split(/\r?\n/), paths = String(v['in'] || '').split(/\r?\n/).map(function (s) { return s.replace(/^\.\//, '').replace(/\\/g, '/'); }).filter(function (s) { return s.trim() !== ''; });
    if (!paths.length) throw new Error(t('경로를 입력하세요', 'Enter some paths'));
    var notes = [], gi = o.mode === 'gitignore';
    function expandBraces(s) {
      var depth = 0, start = -1;
      for (var i = 0; i < s.length; i++) {
        if (s[i] === '\\') { i++; continue; }
        if (s[i] === '{') { if (depth === 0) start = i; depth++; }
        else if (s[i] === '}' && depth > 0) {
          depth--;
          if (depth === 0) {
            var inner = s.slice(start + 1, i), parts = [], d = 0, cur = '';
            for (var j = 0; j < inner.length; j++) { var c = inner[j]; if (c === '\\') { cur += c + (inner[j + 1] || ''); j++; continue; } if (c === '{') d++; if (c === '}') d--; if (c === ',' && d === 0) { parts.push(cur); cur = ''; } else cur += c; }
            parts.push(cur);
            var range = /^(-?\d+)\.\.(-?\d+)$/.exec(inner);
            if (parts.length === 1 && range) { parts = []; var a = +range[1], b = +range[2], step = a <= b ? 1 : -1; for (var n = a; step > 0 ? n <= b : n >= b; n += step) parts.push(String(n)); if (parts.length > 500) parts = parts.slice(0, 500); }
            else if (parts.length === 1) continue;
            var pre = s.slice(0, start), post = s.slice(i + 1), out = [];
            parts.forEach(function (p) { expandBraces(pre + p + post).forEach(function (x) { out.push(x); }); });
            return out;
          }
        }
      }
      return [s];
    }
    function toRegex(g, anchored, dirOnly) {
      var re = '', i = 0, n = g.length;
      while (i < n) {
        var c = g[i];
        if (c === '*') {
          if (g[i + 1] === '*') {
            var atStart = i === 0 || g[i - 1] === '/';
            if (atStart && (g[i + 2] === '/' || i + 2 === n)) {
              var dotGuard = o.dot || gi ? '' : '(?!\\.)';
              if (g[i + 2] === '/') { re += '(?:(?:' + dotGuard + '[^/]*)/)*'; i += 3; } else { re += '.*'; i += 2; }
              continue;
            }
            re += '[^/]*'; i += 2; continue;
          }
          re += (i === 0 || g[i - 1] === '/') && !o.dot && !gi ? '(?!\\.)[^/]*' : '[^/]*'; i++; continue;
        }
        if (c === '?') { re += (i === 0 || g[i - 1] === '/') && !o.dot && !gi ? '(?!\\.)[^/]' : '[^/]'; i++; continue; }
        if (c === '[') {
          var j = i + 1; if (g[j] === '!' || g[j] === '^') j++; if (g[j] === ']') j++;
          while (j < n && g[j] !== ']') { if (g[j] === '\\') j++; j++; }
          if (j >= n) { re += '\\['; i++; continue; }
          var body = g.slice(i + 1, j).replace(/^!/, '^').replace(/\\(?!\\)/g, '\\\\');
          var posix = { 'alpha': 'A-Za-z', 'digit': '0-9', 'alnum': 'A-Za-z0-9', 'upper': 'A-Z', 'lower': 'a-z', 'space': '\\s', 'punct': '!-\\/:-@\\[-`{-~' };
          body = body.replace(/\[:([a-z]+):\]/g, function (m, nm) { return posix[nm] || m; });
          re += '[' + body + ']'; i = j + 1; continue;
        }
        if (c === '\\' && i + 1 < n) { re += g[i + 1].replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&'); i += 2; continue; }
        if ((c === '+' || c === '@' || c === '!' || c === '?' || c === '*') && g[i + 1] === '(') { /* extglob 미지원 */ }
        re += c.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&'); i++;
      }
      return re;
    }
    var rules = [];
    rawPats.forEach(function (line, idx) {
      var p = line.replace(/\s+$/, '');
      if (!p || (p[0] === '#' && (gi || p[1] !== '!')) ) return;
      var neg = false;
      if (p[0] === '!') { neg = true; p = p.slice(1); }
      else if (p.indexOf('\\!') === 0 || p.indexOf('\\#') === 0) p = p.slice(1);
      if (!p) return;
      var dirOnly = false, anchored = false, hasSlash;
      if (gi) {
        if (/\/$/.test(p)) { dirOnly = true; p = p.replace(/\/+$/, ''); }
        hasSlash = p.indexOf('/') >= 0;
        if (p[0] === '/') { anchored = true; p = p.slice(1); } else if (hasSlash) anchored = true;
      } else if (p[0] === '/') p = p.slice(1);
      expandBraces(p).forEach(function (g) {
        var body = toRegex(g, anchored, dirOnly), src;
        if (gi) src = anchored ? '^' + body + '(?:/.*)?$' : '^(?:.*/)?' + body + '(?:/.*)?$';
        else src = '^' + body + '$';
        var rx; try { rx = new RegExp(src, o.nocase ? 'i' : ''); } catch (e) { notes.push('⛔ ' + t('패턴 ' + (idx + 1) + ' 줄 "' + line + '": 정규식으로 바꿀 수 없습니다 (' + e.message + ')', 'Pattern on line ' + (idx + 1) + ' "' + line + '" cannot be converted (' + e.message + ')')); return; }
        rules.push({ line: idx + 1, text: line, neg: neg, rx: rx, src: src, dirOnly: dirOnly });
      });
    });
    if (!rules.length) throw new Error(t('패턴을 입력하세요', 'Enter at least one pattern'));
    function isDir(p, all) { return /\/$/.test(p) || all.some(function (q) { return q !== p && q.indexOf(p.replace(/\/$/, '') + '/') === 0; }); }
    var matched = [], rows = [];
    paths.forEach(function (p) {
      var clean = p.replace(/\/$/, ''), res = false, by = '';
      if (gi) {
        /* 상위 디렉터리가 무시되면 하위 항목은 ! 로 되살릴 수 없다 */
        var segs = clean.split('/'), blockedBy = null;
        for (var k = 1; k <= segs.length && !blockedBy; k++) {
          var sub = segs.slice(0, k).join('/'), dirLike = k < segs.length || isDir(p, paths), lastR = null;
          rules.forEach(function (r) { if (r.dirOnly && !dirLike) return; if (r.rx.test(sub)) lastR = r; });
          if (k < segs.length) { if (lastR && !lastR.neg) blockedBy = lastR; }
          else if (lastR) { res = !lastR.neg; by = lastR.text; }
        }
        if (blockedBy) { res = true; by = blockedBy.text + ' ' + t('(상위 폴더)', '(parent folder)'); }
      } else {
        /* minimatch: 일치하는 일반 패턴이 하나라도 있고, 일치하는 ! 패턴이 없으면 포함 */
        var inc = rules.filter(function (r) { return !r.neg && r.rx.test(clean); })[0], excl = rules.filter(function (r) { return r.neg && r.rx.test(clean); })[0];
        res = !!inc && !excl; by = excl ? excl.text : (inc ? inc.text : '');
      }
      rows.push([p, res ? (gi ? '🚫 ' + t('무시됨', 'ignored') : '✅ ' + t('일치', 'match')) : (gi ? '✅ ' + t('추적됨', 'tracked') : '— ' + t('불일치', 'no match')), by || '—']);
      if (res) matched.push(p);
    });
    var rxRows = rules.map(function (r) { return [r.text, r.src]; });
    if (!gi && !o.dot && paths.some(function (p) { return /(^|\/)\./.test(p); })) notes.push('ℹ️ ' + t('점(.)으로 시작하는 경로는 * 와 ** 에 기본으로 일치하지 않습니다. 필요하면 "점 파일도 일치"를 켜거나 패턴에 .* 를 직접 쓰세요', 'Paths starting with a dot are not matched by * and ** by default; enable "match dotfiles" or write .* explicitly'));
    if (gi) notes.push('ℹ️ ' + t('.gitignore 규칙: 패턴에 /가 없으면 모든 깊이에서 이름이 일치하고, 끝이 /면 폴더만, 앞이 /면 루트 기준입니다. 상위 폴더가 무시되면 ! 로 되살릴 수 없습니다', '.gitignore rules: a pattern without / matches at any depth, a trailing / matches folders only and a leading / anchors to the root. A file inside an ignored folder cannot be re-included with !'));
    else notes.push('ℹ️ ' + t('{a,b} 중괄호와 {1..3} 범위, [abc] 문자 집합, ** 모든 깊이를 지원합니다. extglob(@(a|b)) 는 지원하지 않습니다', '{a,b} braces, {1..3} ranges, [abc] sets and ** are supported; extglob (@(a|b)) is not'));
    return { _status: t('✅ ' + paths.length + '개 중 ' + matched.length + '개 ' + (gi ? '무시됨' : '일치'), '✅ ' + matched.length + ' of ' + paths.length + (gi ? ' ignored' : ' matched')), res: { head: [['경로', 'Path'], ['결과', 'Result'], ['결정한 규칙', 'Deciding rule']], rows: rows }, rx: { head: [['패턴', 'Pattern'], ['정규식', 'Regex']], rows: rxRows }, out: matched.join('\n'), issues: notes };
  }
});
