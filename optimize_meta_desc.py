"""
WooaText KO 페이지 메타 디스크립션 CTR 최적화
- 최우선: "글자 변환"(82)+"글자변환"(19) = 101 노출 → case-converter.html
- 핵심: "단어 수 세기"(53)+"한글파일 글자수 세기"(38)+"글자수 카운트"(37) = 128 노출 → char-counter.html
- 기타: 더미텍스트(30), sha256 해시값(12), 마크다운 포맷(10), base64(7), html 특수문자(4)
- 공통: "설치 없이 브라우저에서 무료로 사용 가능합니다" 보일러플레이트 제거
"""
import re, os

BASE = 'C:/개인/wooahouse/TextKit'

PAGES = {
    # ── index ───────────────────────────────────────────────────────────
    'index.html': (
        '글자수 세기, 텍스트 비교, 대소문자 변환',
        '글자수 세기·글자 변환·단어 수 세기·텍스트 비교·URL 인코딩·Base64·JSON 포맷터·해시 생성·마크다운 에디터까지 무료! 설치·로그인 없이 브라우저에서 바로 — 우아텍스트(WooaText)'
    ),
    # ── 101 노출 0% CTR: 최우선 ─────────────────────────────────────────
    'case-converter.html': (
        '텍스트를 UPPERCASE, lowercase, Title Case',
        '글자 변환·대소문자 변환기 무료 — UPPERCASE·lowercase·Title Case·camelCase·snake_case·kebab-case로 즉시 변환. 개발자·작가 모두에게 유용, 설치·로그인 없이 바로 사용.'
    ),
    # ── 128 노출 0% CTR: 중요 ────────────────────────────────────────────
    'char-counter.html': (
        '텍스트의 글자수, 단어수, 줄수, 문장수, 단락수를 실시간으로 카운트',
        '글자수 세기·단어 수 세기 무료 — 글자수·단어수·문장수·단락수를 실시간 카운트. 한글파일 글자수 세기 지원, 공백 포함/제외 선택, 설치·로그인 없이 바로 사용.'
    ),
    # ── 더미텍스트 30 노출 ────────────────────────────────────────────────
    'lorem-ipsum.html': (
        'Lorem Ipsum 더미 텍스트를 단락·문장·단어 단위로 생성',
        '더미 텍스트·Lorem Ipsum 생성기 무료 — 단락·문장·단어 단위로 즉시 생성, 한국어 더미 텍스트도 지원. 디자인 목업·웹 개발에 최적, 설치·로그인 없이 바로 사용.'
    ),
    # ── sha256 해시값 12 노출 ─────────────────────────────────────────────
    'hash-generator.html': (
        '텍스트의 SHA-256, SHA-1, SHA-512, MD5 해시값을 브라우저에서 직접 생성',
        'SHA256 해시값 생성기 무료 — SHA-256·SHA-1·SHA-512·MD5 해시를 브라우저에서 즉시 생성. 서버 전송 없이 100% 안전하게 처리, 설치·로그인 없이 바로 사용.'
    ),
    # ── 마크다운 포맷 10 노출 ────────────────────────────────────────────
    'markdown-editor.html': (
        '마크다운을 실시간으로 HTML로 변환하며 미리보기',
        '마크다운 에디터·마크다운 포맷 변환 무료 — 실시간 HTML 미리보기, 마크다운 기호 모음 참조. 코드 하이라이팅·파일 저장 지원, 설치·로그인 없이 바로 사용.'
    ),
    # ── base64 7 노출 ─────────────────────────────────────────────────────
    'base64.html': (
        '텍스트를 Base64로 인코딩하거나 Base64를 텍스트로 디코딩',
        'Base64 변환기 무료 — 텍스트·URL·이미지를 Base64로 인코딩/디코딩 즉시 변환. 한글 유니코드 완벽 지원, 설치·로그인 없이 바로 사용.'
    ),
    # ── html 특수문자 4 노출 ──────────────────────────────────────────────
    'html-entity.html': (
        'HTML 특수문자',
        'HTML 특수문자 변환기 무료 — &·<·>·"·\' 등 HTML 엔티티를 인코딩/디코딩으로 즉시 변환. 웹 개발에 필수, 설치·로그인 없이 바로 사용.'
    ),
    # ── 나머지 전체 (보일러플레이트 제거 + 키워드 선행) ───────────────────
    'text-stats.html': (
        '텍스트의 글자수, 단어 수, 문장 수, 단어 빈도 Top20',
        '텍스트 통계 분석기 무료 — 글자수·단어수·문장수·단어 빈도 Top20을 실시간 분석. 블로그·논문 가독성 분석에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'url-encoder.html': (
        'URL 인코딩(encodeURIComponent)과 디코딩',
        'URL 인코딩·디코딩 변환기 무료 — encodeURIComponent·decodeURIComponent를 온라인으로 즉시 변환. 한글·특수문자 포함 URL 처리, 설치·로그인 없이 바로 사용.'
    ),
    'unicode-converter.html': (
        '텍스트를 Unicode escape',
        '유니코드 변환기 무료 — 텍스트를 Unicode escape·HTML 엔티티·코드포인트로 즉시 변환. 한글·이모지 완벽 지원, 설치·로그인 없이 바로 사용.'
    ),
    'text-diff.html': (
        '두 텍스트를 비교해서 추가·삭제·변경된 부분을 색으로 강조 표시',
        '텍스트 비교·Diff 도구 무료 — 두 텍스트의 추가·삭제·변경 부분을 색으로 즉시 강조 표시. 코드 리뷰·문서 수정사항 확인에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'text-replacer.html': (
        '텍스트에서 특정 단어를 찾아 일괄 치환',
        '텍스트 찾기·치환기 무료 — 특정 단어를 찾아 일괄 치환, 정규식·대소문자 무시·여러 규칙 동시 지원. 반복 편집 자동화에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'line-tools.html': (
        '텍스트 줄을 오름차순·내림차순 정렬, 중복 줄 제거',
        '텍스트 줄 정리 도구 무료 — 오름차순·내림차순 정렬, 중복 줄 제거, 빈 줄 제거, 줄 뒤집기·무작위 섞기. CSV·코드 데이터 정리에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'whitespace.html': (
        '텍스트 앞뒤 공백 제거, 연속 공백을 하나로',
        '공백 제거·정리 도구 무료 — 앞뒤 공백 제거, 연속 공백을 하나로, 탭을 스페이스로 변환. 텍스트 데이터 정리에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'slug-generator.html': (
        '텍스트를 URL에 사용할 수 있는 슬러그(slug)로 변환',
        'URL 슬러그 생성기 무료 — 텍스트를 SEO 친화적인 slug로 즉시 변환. 한글 음역·구분자·대소문자 옵션 지원, 설치·로그인 없이 바로 사용.'
    ),
    'password-generator.html': (
        '길이와 문자 종류를 설정해 안전한 비밀번호를 생성',
        '비밀번호 생성기 무료 — 길이·문자 종류를 설정해 안전한 비밀번호를 즉시 생성. 강도 측정기·여러 개 동시 생성 지원, 설치·로그인 없이 바로 사용.'
    ),
    'json-formatter.html': (
        'JSON을 보기 좋게 정렬하거나 압축하고 유효성을 검사',
        'JSON 포맷터·유효성 검사기 무료 — JSON을 보기 좋게 정렬하거나 압축, 오류 줄 번호 즉시 표시. 개발자 필수 도구, 설치·로그인 없이 바로 사용.'
    ),
    'regex-tester.html': (
        '정규식(Regex)을 실시간으로 테스트',
        '정규식 테스터 무료 — 매칭 결과 하이라이팅, 그룹 캡처, 치환, 빠른 패턴 모음 지원. 한국어 포함 다국어 정규식 테스트, 설치·로그인 없이 바로 사용.'
    ),
    'csv-json.html': (
        'CSV를 JSON으로, JSON을 CSV로 무료 변환',
        'CSV·JSON 변환기 무료 — CSV를 JSON으로, JSON을 CSV로 즉시 변환. 파일 업로드·텍스트 직접 입력 지원, 설치·로그인 없이 바로 사용.'
    ),
    'html-css-editor.html': (
        'HTML, CSS, JavaScript를 브라우저에서 바로 작성하고 실시간으로 미리보기',
        '온라인 HTML·CSS·JS 에디터 무료 — 브라우저에서 바로 코드를 작성하고 실시간 미리보기. 다크모드 지원, 회원가입·설치 없이 바로 사용.'
    ),
    'jwt-decoder.html': (
        'JWT 토큰을 붙여넣으면 Header, Payload, Signature를 자동 파싱',
        'JWT 토큰 디코더 무료 — Header·Payload·Signature를 자동 파싱, 만료일시·남은 시간 즉시 표시. 브라우저에서 100% 로컬 처리로 안전, 설치·로그인 없이 바로 사용.'
    ),
    'xml-formatter.html': (
        'XML을 들여쓰기 정렬하거나 압축하고 유효성을 검사',
        'XML 포맷터·유효성 검사기 무료 — XML을 들여쓰기 정렬하거나 압축, 신탁스 하이라이팅 포함. RSS·SOAP·설정 파일 편집에 최적, 설치·로그인 없이 바로 사용.'
    ),
    'yaml-json.html': (
        'YAML을 JSON으로, JSON을 YAML로 즉시 변환',
        'YAML·JSON 변환기 무료 — YAML을 JSON으로, JSON을 YAML로 즉시 변환. 유효성 검사·실시간 변환 지원, 설치·로그인 없이 바로 사용.'
    ),
    'html-markdown.html': (
        'HTML을 마크다운으로, 마크다운을 HTML로 상호 변환',
        'HTML·마크다운 상호 변환기 무료 — HTML을 마크다운으로, 마크다운을 HTML로 클릭 한 번에 즉시 변환. 설치·로그인 없이 바로 사용.'
    ),
    'morse-code.html': (
        '텍스트를 모스부호로, 모스부호를 텍스트로 상호 변환',
        '모스부호 변환기 무료 — 텍스트를 모스부호로, 모스부호를 텍스트로 즉시 변환. Web Audio API 신호음 재생, 설치·로그인 없이 바로 사용.'
    ),
    'number-base.html': (
        '이진수, 8진수, 10진수, 16진수를 실시간으로 상호 변환',
        '진법 변환기 무료 — 이진수·8진수·10진수·16진수를 실시간 상호 변환. 어느 칸을 입력해도 나머지가 자동 변환, 설치·로그인 없이 바로 사용.'
    ),
    'line-numbering.html': (
        '각 줄에 번호나 글머리 기호를 자동으로 추가',
        '줄 번호 매기기 도구 무료 — 각 줄에 번호·원문자·불릿을 자동 추가. 시작 번호 설정·다양한 형식 지원, 설치·로그인 없이 바로 사용.'
    ),
    'timestamp-converter.html': (
        'Unix timestamp를 날짜시간으로, 날짜시간을 timestamp로 변환',
        '타임스탬프 변환기 무료 — Unix timestamp를 날짜시간으로, 날짜시간을 timestamp로 즉시 변환. 초/밀리초 자동 감지, 설치·로그인 없이 바로 사용.'
    ),
}

ok_count = 0
fail_count = 0

for fname, (match_prefix, new_desc) in PAGES.items():
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        print(f'  SKIP (없음): {fname}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(<meta name="description" content=")[^"]*(")'

    def desc_replacer(m):
        if match_prefix in m.group(0):
            return m.group(1) + new_desc + m.group(2)
        return m.group(0)

    new_content = re.sub(pattern, desc_replacer, content)

    if new_content == content:
        print(f'  MISS: {fname} — "{match_prefix[:40]}"')
        fail_count += 1
        continue

    new_content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2), new_content
    )
    new_content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_desc + x.group(2), new_content
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  OK: {fname}')
    ok_count += 1

print(f'\n완료: {ok_count}개 교체, {fail_count}개 실패')
