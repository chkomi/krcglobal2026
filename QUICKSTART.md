# 🚀 빠른 시작 가이드

## 시스템 실행 방법

### 방법 1: 시작 스크립트 사용 (권장)

```bash
./start.sh
```

이 스크립트는 자동으로:
- 백엔드 서버 (Flask) 실행: `http://localhost:5000`
- 프론트엔드 서버 실행: `http://localhost:8000`

### 방법 2: 수동 실행

**백엔드 서버:**
```bash
cd backend
python app.py
```

**프론트엔드 서버 (새 터미널):**
```bash
python -m http.server 8000
```

## 접속 방법

브라우저에서 다음 주소로 접속:
```
http://localhost:8000/index.html
```

## 로그인

- **아이디**: 아무거나 입력
- **비밀번호**: 아무거나 입력
- 데모 모드로 모든 입력을 허용합니다

## 주요 페이지

- **대시보드**: `http://localhost:8000/dashboard.html`
- **해외기술용역**: `http://localhost:8000/pages/projects/overseas-tech.html`
- **GIS 지도**: `http://localhost:8000/pages/gis.html`

## 문제 해결

### UI가 일관되지 않은 경우

1. 브라우저 캐시 삭제:
   - Chrome: `Cmd + Shift + Delete` (Mac) / `Ctrl + Shift + Delete` (Windows)
   - 또는 시크릿 모드로 접속

2. 올바른 URL 확인:
   - ✅ `http://localhost:8000/index.html`
   - ❌ `http://localhost:8000/frontend/index.html`

### 로그인이 풀리는 경우

- "로그인 상태 유지" 체크박스를 선택하세요
- 브라우저의 쿠키/로컬 스토리지를 허용해야 합니다

## 디렉토리 구조

```
krcglobal2026/
├── index.html          ← 로그인 페이지 (여기서 시작)
├── dashboard.html      ← 메인 대시보드
├── assets/            ← CSS, JS, 이미지
├── pages/             ← 모든 기능 페이지
│   ├── projects/      ← 사업관리
│   ├── gis.html       ← GIS 지도
│   └── consulting.html
└── backend/           ← Flask API 서버
```

## 주의사항

⚠️ **frontend/ 디렉토리는 레거시 파일입니다. 사용하지 마세요!**

- 새로운 KRDS 디자인은 루트의 `index.html`, `dashboard.html`을 사용합니다
- 모든 페이지는 `pages/` 디렉토리에 있습니다
