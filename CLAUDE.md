# TextKit 프로젝트 지침

## 프로젝트 개요
- **사이트명:** 텍스트킷 (TextKit)
- **URL:** https://textkit.wooahouse.com
- **GitHub:** https://github.com/ingmaster83-code/TextKit
- **배포:** GitHub Pages (main 브랜치 → root)

## 기술 스택
- 순수 HTML / CSS / JS (프레임워크 없음)
- PWA: manifest.json + sw.js + js/pwa-install.js

## 서비스 목적
텍스트 분석·변환·정리·생성 도구를 브라우저에서 무료로 제공.

## 도구 목록 (15개)
글자수세기, 텍스트비교(diff), 대소문자변환, URL인코딩, Base64변환, HTML엔티티,
줄정렬·중복제거, 공백제거, Lorem Ipsum, 비밀번호생성기, JSON포맷터, 해시생성기,
**마크다운에디터**(marked.js+highlight.js), **정규식테스터**, **CSV↔JSON변환**(PapaParse)
*굵은 글씨 = 최근 추가*

## 작업 규칙
- 새 도구 추가 시 index.html 카드, sitemap.xml 업데이트 필수
- SEO 키워드: 글자수 세기, 텍스트 변환, JSON 포맷터, 비밀번호 생성기, 마크다운 에디터
