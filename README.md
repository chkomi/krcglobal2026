# GBMS - 글로벌사업처 해외사업관리시스템

한국농어촌공사 글로벌사업처의 해외사업을 통합 관리하는 웹 시스템입니다.

## 📋 주요 기능

- **대시보드**: 전체 사업 현황 한눈에 파악
- **사업관리**: 해외기술용역, ODA(양자/다자성양자), K-라이스벨트, 해외농업투자 등
- **예산/정산**: 사업별 예산 배정 및 집행 관리
- **문서관리**: 사업 관련 문서 통합 관리
- **해외사무소**: 사무소 현황 및 운영 관리
- **인력관리**: 용역단 및 파견인력 관리
- **성과관리**: KPI 설정 및 달성률 추적

## 🛠️ 기술 스택

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite (WAL 모드, 100명 동시접속 지원)

## 📁 디렉토리 구조

```
해외사업관리시스템/
├── frontend/                # 프론트엔드
│   ├── index.html          # 로그인 페이지
│   ├── dashboard.html      # 대시보드
│   ├── css/               # 스타일시트
│   ├── js/                # JavaScript
│   └── pages/             # 서브 페이지
│
├── backend/                # 백엔드
│   ├── app.py             # Flask 메인
│   ├── config.py          # 설정
│   ├── models/            # 데이터베이스 모델
│   ├── routes/            # API 라우트
│   ├── init_db.py         # DB 초기화
│   └── requirements.txt   # Python 의존성
│
└── README.md
```

## 🚀 설치 및 실행

### 내부망 오프라인 설치

1. **외부망 PC에서 패키지 다운로드**
```bash
pip download -r backend/requirements.txt -d ./packages
```

2. **내부망 서버에서 설치**
```bash
pip install --no-index --find-links=./packages -r backend/requirements.txt
```

3. **데이터베이스 초기화**
```bash
cd backend
python init_db.py
```

4. **서버 실행**
```bash
python app.py
```

5. **브라우저에서 접속**
```
http://localhost:5000
```

### 테스트 계정

| 아이디 | 비밀번호 | 권한 | 부서 |
|--------|----------|------|------|
| admin | admin123 | 관리자 | 글로벌농업개발부 |
| user1 | user123 | 일반 | 글로벌사업부 |
| user2 | user123 | 일반 | 농식품국제개발협력센터 |

## 📡 API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/auth/login` | 로그인 |
| GET | `/api/projects` | 사업 목록 |
| POST | `/api/projects` | 사업 등록 |
| GET | `/api/budgets/stats` | 예산 통계 |
| POST | `/api/documents/upload` | 문서 업로드 |
| GET | `/api/dashboard/overview` | 대시보드 개요 |

## ⚙️ 운영 환경

### 권장 서버 사양
- **OS**: Windows Server 2019+ 또는 Ubuntu 20.04+
- **CPU**: 4코어 이상
- **RAM**: 8GB 이상
- **Storage**: 500GB 이상

### 백업
- 일일: `backend/database/gbms.db` 자동 백업
- 주간: 전체 시스템 백업
- 월간: 오프사이트 백업

## 📞 문의

글로벌농업개발부 시스템담당 (내선: 1234)

---

© 2024 한국농어촌공사 글로벌사업처
