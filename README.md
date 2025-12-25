# KRC Global 2026 - 해외사업관리시스템 (GBMS)

한국농어촌공사 글로벌사업처 해외사업관리시스템 - KRDS 기반 고도화 버전

## 🎨 디자인 시스템

**Korea Design System (KRDS)** 철학을 기반으로 한 일관성 있는 디자인

### 주요 색상
- **Primary (네이비 블루)**: `#1A4B7C` - KRC 브랜드 색상
- **Secondary (상아색)**: `#CEC0AC` - 따뜻하고 전문적인 느낌
- **Neutral (그레이/검정)**: `#1A1A1A ~ #FFFFFF` - 텍스트 및 배경

### 타이포그래피
- **Font Family**: Pretendard, Noto Sans KR
- **Font Sizes**: 12px ~ 36px (8단계)
- **Font Weights**: 400, 500, 600, 700

## 📁 프로젝트 구조

```
krcglobal2026/
├── index.html              # 로그인 페이지
├── dashboard.html          # 메인 대시보드
├── assets/
│   ├── css/
│   │   ├── variables.css   # 디자인 토큰
│   │   ├── base.css        # 기본 스타일
│   │   ├── components.css  # 컴포넌트 스타일
│   │   └── pages.css       # 페이지 레이아웃
│   ├── js/
│   │   ├── common.js       # 공통 유틸리티
│   │   ├── api.js          # API 통신
│   │   └── components/
│   │       ├── modal.js    # 모달 컴포넌트
│   │       └── toast.js    # 토스트 알림
│   └── images/
├── pages/
│   ├── projects/           # 사업관리
│   │   ├── overseas-tech.html
│   │   ├── oda-bilateral.html
│   │   ├── oda-multilateral.html
│   │   ├── k-rice-belt.html
│   │   └── overseas-investment.html
│   ├── budget/             # 예산/정산
│   ├── documents/          # 문서관리
│   ├── offices/            # 해외사무소
│   ├── personnel/          # 인력관리
│   └── performance/        # 성과관리
├── backend/                # Flask 백엔드
└── frontend/               # 레거시 파일 (참고용)
```

## 🚀 시작하기

### 백엔드 서버 실행

```bash
cd backend
python app.py
```

### 프론트엔드 접속

브라우저에서 `index.html` 파일을 직접 열거나, 로컬 서버를 실행:

```bash
# Python 간단 서버
python -m http.server 8000

# 브라우저에서 접속
http://localhost:8000
```

## ✨ 주요 기능

### 1. 로그인 시스템
- 사번/아이디 기반 인증
- 로그인 상태 유지 (Remember Me)
- 접근성 강화 (ARIA, 키보드 네비게이션)

### 2. 대시보드
- 실시간 통계 카드 (진행중 사업, 예산, 대상국, 사무소)
- 최근 사업 현황 테이블
- 반응형 레이아웃

### 3. 사업관리
- **해외기술용역**: 검색/필터, 통계, CRUD
- **ODA 양자/다자성양자**: 국제협력사업 관리
- **K-라이스벨트**: 식량안보 사업
- **해외농업투자**: 투자사업 관리

### 4. 예산/정산
- 예산 현황 대시보드
- 부서별 집행률 차트
- 정산 요청 워크플로우

### 5. 문서관리
- 폴더 트리 네비게이션
- 드래그 앤 드롭 업로드
- 문서 검색 및 필터링

### 6. 해외사무소
- GIS 지도 연동 (Leaflet)
- 사무소 현황 카드
- 인력 배치 현황

### 7. 인력관리
- 인력 DB 관리
- 계약 현황 추적
- 출장 일정 관리

### 8. 성과관리
- KPI 대시보드
- 실시간 달성률 추적
- 자동 보고서 생성

## 🎯 접근성 (Accessibility)

- **WCAG 2.1 AA 준수**
- 키보드 네비게이션 완벽 지원
- 스크린 리더 호환 (ARIA 속성)
- 스킵 네비게이션
- 포커스 인디케이터
- 색상 대비 최적화

## 📱 반응형 디자인

- **Desktop**: > 1200px
- **Tablet**: 768px ~ 1200px
- **Mobile**: < 768px

## 🛠️ 기술 스택

### Frontend
- HTML5
- CSS3 (CSS Variables, Grid, Flexbox)
- Vanilla JavaScript (ES6+)
- Pretendard Font

### Backend
- Python Flask
- SQLite
- RESTful API

### Libraries
- Leaflet (GIS 지도)

## 📝 개발 가이드

### CSS 변수 사용

```css
/* 색상 */
color: var(--color-primary-500);
background: var(--color-secondary-100);

/* 간격 */
padding: var(--spacing-4);
margin: var(--spacing-6);

/* 타이포그래피 */
font-size: var(--font-size-lg);
font-weight: var(--font-weight-semibold);
```

### 컴포넌트 사용

```javascript
// Toast 알림
Toast.success('저장되었습니다.');
Toast.error('오류가 발생했습니다.');

// Modal
const modal = new Modal();
modal.open('<p>내용</p>', '제목');
```

## 🔄 업데이트 내역

### 2024-12-25
- KRDS 디자인 시스템 적용
- 프로젝트 구조 재편
- 접근성 강화
- 반응형 디자인 구현
- JavaScript 컴포넌트 모듈화

## 📞 문의

글로벌농업개발부 내선 1234

---

© 2024-2026 한국농어촌공사 글로벌사업처
