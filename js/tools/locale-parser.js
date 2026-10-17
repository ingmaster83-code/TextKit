TK.tool('locale-parser', {
  sampleExpectError: true,
  inputs: [{ id: 'in', label: ['로케일 태그 (BCP 47) — 한 줄에 하나', 'Locale tags (BCP 47) - one per line'], rows: 6, sample: 'ko-KR\nen-US\nzh-Hant-TW\nsr-Latn-RS\nko-KR-u-ca-gregory-nu-hanidec\nar-EG\nde_CH\nxx-INVALID-' }],
  options: [
    { id: 'show', type: 'select', label: ['표시 언어', 'Names in'], choices: [['ko', '한국어'], ['en', 'English'], ['ja', '日本語'], ['zh', '中文']], default: 'ko' },
    { id: 'when', type: 'text', label: ['서식 예시 기준 시각 (ISO, 비우면 2026-10-17T13:05:09Z)', 'Sample time for formatting (ISO; default 2026-10-17T13:05:09Z)'], default: '' }
  ],
  outputs: [{ id: 'table', label: ['구성 요소', 'Components'], kind: 'table' }, { id: 'fmt', label: ['서식 예시', 'Formatting samples'], kind: 'table' }, { id: 'issues', label: ['점검 결과', 'Findings'], kind: 'list' }],
  run: function (v, o, t) {
    if (typeof Intl === 'undefined' || !Intl.Locale) throw new Error(t('이 브라우저는 Intl.Locale 을 지원하지 않습니다', 'This browser does not support Intl.Locale'));
    var tags = String(v['in'] || '').split(/\r?\n/).map(function (s) { return s.trim(); }).filter(Boolean).slice(0, 40);
    if (!tags.length) throw new Error(t('로케일 태그를 입력하세요', 'Enter at least one locale tag'));
    var when = String(o.when || '').trim() ? new Date(String(o.when).trim()) : new Date('2026-10-17T13:05:09Z');
    if (isNaN(when)) throw new Error(t('기준 시각 형식이 올바르지 않습니다', 'Invalid sample time'));
    var disp = o.show || 'ko';
    function dn(type, code) { try { return new Intl.DisplayNames([disp], { type: type, fallback: 'none' }).of(code) || ''; } catch (e) { return ''; } }
    var rows = [], fmt = [], notes = [];
    tags.forEach(function (raw) {
      var fixed = raw.replace(/_/g, '-');
      var loc;
      try { loc = new Intl.Locale(fixed); } catch (e) { rows.push([raw, '⛔ ' + t('유효하지 않음', 'invalid'), '', '', '', '', '', '', '']); notes.push('⛔ ' + t('"' + raw + '" 은(는) 올바른 BCP 47 태그가 아닙니다 (' + e.message + ')', '"' + raw + '" is not a valid BCP 47 tag (' + e.message + ')')); return; }
      var canon = loc.toString(), mx = loc.maximize(), mn = loc.minimize();
      if (raw !== canon && fixed === raw) notes.push('ℹ️ ' + t('"' + raw + '" → 표준형 "' + canon + '" (대소문자·순서 정리)', '"' + raw + '" → canonical "' + canon + '" (case and order normalised)'));
      if (raw.indexOf('_') >= 0) notes.push('⚠️ ' + t('"' + raw + '" 의 밑줄(_)은 POSIX/Java 형식입니다. BCP 47 은 하이픈(-)을 씁니다 → "' + canon + '"', '"' + raw + '": the underscore is POSIX / Java style; BCP 47 uses a hyphen -> "' + canon + '"'));
      var supported = Intl.NumberFormat.supportedLocalesOf([canon]).length > 0;
      var lang = loc.language, script = loc.script || '', region = loc.region || '';
      var langName = dn('language', lang), scrName = script ? dn('script', script) : '', regName = region ? dn('region', region) : '';
      var ext = []; ['calendar', 'collation', 'hourCycle', 'caseFirst', 'numeric', 'numberingSystem'].forEach(function (k) { if (loc[k] !== undefined && loc[k] !== null && loc[k] !== false) ext.push(k + '=' + loc[k]); });
      var dir = ''; try { var ti = loc.getTextInfo ? loc.getTextInfo() : loc.textInfo; dir = ti && ti.direction ? ti.direction : (/^(ar|he|fa|ur|ps|sd|yi|ug|dv)$/.test(lang) ? 'rtl' : 'ltr'); } catch (e) { dir = /^(ar|he|fa|ur|ps|sd|yi|ug|dv)$/.test(lang) ? 'rtl' : 'ltr'; }
      rows.push([raw, canon, langName ? lang + ' (' + langName + ')' : lang, script ? script + (scrName ? ' (' + scrName + ')' : '') : '—', region ? region + (regName ? ' (' + regName + ')' : '') : '—', ext.join(', ') || '—', mx.toString() + ' / ' + mn.toString(), dir, supported ? '✅' : '⚠️ ' + t('이 브라우저에 데이터 없음', 'no data in this browser')]);
      if (!script && !region && mx.script) notes.push('ℹ️ ' + t('"' + canon + '" 에 스크립트·지역이 없어 브라우저가 ' + mx.toString() + ' 로 추정합니다', '"' + canon + '" has no script / region, so the engine assumes ' + mx.toString()));
      if (!langName && lang) notes.push('⚠️ ' + t('언어 코드 "' + lang + '" 의 이름을 찾지 못했습니다. 존재하지 않는 코드일 수 있습니다', 'No name found for language "' + lang + '"; it may not exist'));
      try {
        var pr = new Intl.PluralRules([canon]), cats = pr.resolvedOptions().pluralCategories;
        var pord = new Intl.PluralRules([canon], { type: 'ordinal' }).resolvedOptions().pluralCategories;
        var d1 = new Intl.DateTimeFormat([canon], { dateStyle: 'full', timeStyle: 'short', timeZone: 'UTC' }).format(when);
        var d2 = new Intl.DateTimeFormat([canon], { dateStyle: 'short', timeZone: 'UTC' }).format(when);
        var n1 = new Intl.NumberFormat([canon]).format(1234567.891);
        var cur = region ? ({ US: 'USD', KR: 'KRW', JP: 'JPY', GB: 'GBP', DE: 'EUR', FR: 'EUR', CN: 'CNY', TW: 'TWD', CH: 'CHF', IN: 'INR', BR: 'BRL', EG: 'EGP', RU: 'RUB', CA: 'CAD', AU: 'AUD', ES: 'EUR', IT: 'EUR', RS: 'RSD', MX: 'MXN', SA: 'SAR' }[region] || 'USD') : 'USD';
        var n2 = new Intl.NumberFormat([canon], { style: 'currency', currency: cur }).format(1234.5);
        var n3 = new Intl.NumberFormat([canon], { style: 'percent' }).format(0.256);
        var lst = new Intl.ListFormat([canon], { type: 'conjunction' }).format(['A', 'B', 'C']);
        var rel = new Intl.RelativeTimeFormat([canon], { numeric: 'auto' }).format(-1, 'day');
        var hc = new Intl.DateTimeFormat([canon], { hour: 'numeric', timeZone: 'UTC' }).resolvedOptions().hourCycle;
        var firstDay = ''; try { var wi = loc.getWeekInfo ? loc.getWeekInfo() : loc.weekInfo; if (wi) firstDay = t(['', '월', '화', '수', '목', '금', '토', '일'][wi.firstDay], ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][wi.firstDay]) || ''; } catch (e) { }
        fmt.push([canon, d1, d2, n1, n2 + ' / ' + n3, lst + ' / ' + rel, cats.join(', ') + ' | ' + pord.join(', '), hc + (firstDay ? t(' · 주 시작 ' + firstDay, ' · week starts ' + firstDay) : '')]);
      } catch (e) { fmt.push([canon, '—', '—', '—', '—', '—', '—', e.message]); }
    });
    if (rows.some(function (r) { return /^ko/.test(r[1]) && r[1].indexOf('-u-') >= 0; })) notes.push('ℹ️ ' + t('-u- 뒤는 유니코드 확장입니다 (ca=달력, nu=숫자 체계, hc=시간 주기, co=정렬)', 'The part after -u- is a Unicode extension (ca = calendar, nu = numbering system, hc = hour cycle, co = collation)'));
    var bad = rows.filter(function (r) { return /⛔/.test(r[1]); }).length;
    return { _status: bad ? { ok: false, msg: t('⛔ 유효하지 않은 태그 ' + bad + '개 / ' + tags.length + '개', '⛔ ' + bad + ' invalid of ' + tags.length + ' tag(s)') } : t('✅ ' + tags.length + '개 태그 모두 유효', '✅ All ' + tags.length + ' tag(s) valid'), table: { head: [['입력', 'Input'], ['표준형', 'Canonical'], ['언어', 'Language'], ['스크립트', 'Script'], ['지역', 'Region'], ['확장 옵션', 'Extensions'], ['보완 / 최소화', 'Maximized / minimized'], ['방향', 'Direction'], ['지원', 'Supported']], rows: rows }, fmt: { head: [['로케일', 'Locale'], ['날짜·시간(전체)', 'Date & time (full)'], ['날짜(짧게)', 'Date (short)'], ['숫자', 'Number'], ['통화 / 퍼센트', 'Currency / percent'], ['목록 / 상대 시각', 'List / relative time'], ['복수형 범주 (기수 | 서수)', 'Plural categories (cardinal | ordinal)'], ['시간 주기', 'Hour cycle']], rows: fmt }, issues: notes };
  }
});
