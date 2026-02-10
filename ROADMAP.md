# Roadmap

## Phase 1: 프로젝트 셋업 및 데이터 수집

- [ ] Python 프로젝트 초기화 (pyproject.toml, 의존성 관리)
- [ ] 웹 검색 API 연동 (Tavily 또는 SerpAPI)
- [ ] 경쟁사별 공식 문서/changelog/블로그 크롤링 파이프라인 구축
- [ ] 수집 데이터 로컬 저장 구조 설계 (JSON/SQLite)

## Phase 2: LLM 분석 파이프라인

- [ ] Claude API 연동 (Anthropic SDK)
- [ ] 수집된 원시 데이터를 비교 축별로 구조화하는 프롬프트 설계
- [ ] 경쟁사별 기능 요약 및 비교표 생성 로직
- [ ] Weave 대비 강점/약점 하이라이트 로직

## Phase 3: Markdown 출력 및 GitHub Pages

- [ ] 비교표 Markdown 템플릿 디자인
- [ ] 결과 Markdown 파일 자동 생성 로직
- [ ] GitHub Pages 설정 (Jekyll 또는 정적 사이트)
- [ ] 주차별 리포트 아카이브 구조 (`reports/YYYY-MM-DD.md`)

## Phase 4: 스케줄링 및 자동화

- [ ] 주간 실행 스케줄러 (cron 또는 GitHub Actions)
- [ ] 이전 주 대비 변경사항 diff 표시
- [ ] 실행 결과 알림 (Slack 또는 이메일)
- [ ] GitHub Actions로 리포트 자동 커밋 및 Pages 배포

## Phase 5: 고도화

- [ ] 경쟁사 가격 변동 추적
- [ ] 신규 경쟁사 자동 탐지
- [ ] 히스토리 대시보드 (주차별 트렌드)
