# GIS 지도 기능 설치 가이드

해외사업관리시스템에 GIS 지도 기능을 추가했습니다. 내부망 환경을 고려하여 외부 의존성을 최소화했습니다.

## 설치 방법

### 1. Leaflet 라이브러리 다운로드

**내부망 환경에서는 수동 다운로드가 필요합니다.**

자세한 다운로드 가이드는 `LEAFLET_DOWNLOAD_GUIDE.md` 파일을 참고하세요.

#### 빠른 가이드

외부 인터넷이 연결된 환경에서 다음 5개 파일을 다운로드하세요:

1. `leaflet.css` - https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
2. `leaflet.js` - https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
3. `marker-icon.png` - https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
4. `marker-icon-2x.png` - https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
5. `marker-shadow.png` - https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png

**설치 위치:**
```
frontend/lib/leaflet/leaflet.css
frontend/lib/leaflet/leaflet.js
frontend/lib/leaflet/images/marker-icon.png
frontend/lib/leaflet/images/marker-icon-2x.png
frontend/lib/leaflet/images/marker-shadow.png
```

**디렉토리 생성:**
```bash
mkdir -p frontend/lib/leaflet/images
```

다운로드한 파일들을 해당 위치에 복사하세요.

**외부 인터넷이 연결된 환경에서 다음 파일들을 다운로드하세요:**

1. **Leaflet CSS 파일**
   - URL: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`
   - 저장 위치: `frontend/lib/leaflet/leaflet.css`

2. **Leaflet JavaScript 파일**
   - URL: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`
   - 저장 위치: `frontend/lib/leaflet/leaflet.js`

3. **마커 아이콘 이미지 파일들** (3개)
   - `https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png` → `frontend/lib/leaflet/images/marker-icon.png`
   - `https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png` → `frontend/lib/leaflet/images/marker-icon-2x.png`
   - `https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png` → `frontend/lib/leaflet/images/marker-shadow.png`

**설치 방법:**
1. 외부 인터넷이 연결된 컴퓨터에서 위 URL들을 브라우저로 열어서 파일을 다운로드합니다.
2. 다운로드한 파일들을 ZIP으로 압축하거나 메일로 전송합니다.
3. 내부망 컴퓨터에서 파일을 받아서 다음 디렉토리 구조로 배치합니다:

```
frontend/
  lib/
    leaflet/
      leaflet.css
      leaflet.js
      images/
        marker-icon.png
        marker-icon-2x.png
        marker-shadow.png
```

**디렉토리 생성 명령어 (터미널에서 실행):**
```bash
mkdir -p frontend/lib/leaflet/images
```

그 다음 다운로드한 파일들을 해당 위치에 복사하세요.

### 2. 데이터베이스 마이그레이션

Project 모델에 `latitude`와 `longitude` 필드가 추가되었습니다. 데이터베이스를 업데이트하세요:

```bash
cd backend
python init_db.py
```

또는 기존 데이터베이스가 있는 경우:

```python
from app import app, db
from models import Project

with app.app_context():
    # 기존 테이블에 컬럼 추가 (SQLite의 경우)
    try:
        db.engine.execute('ALTER TABLE projects ADD COLUMN latitude NUMERIC(10,7)')
        db.engine.execute('ALTER TABLE projects ADD COLUMN longitude NUMERIC(10,7)')
    except:
        pass  # 이미 존재하는 경우 무시
```

### 3. 프로젝트 데이터에 좌표 추가

기존 프로젝트에 위도/경도 정보를 추가해야 지도에 표시됩니다. 

KRC 레포지토리의 `data/global_oda.json`과 `data/global_consulting.json` 파일에서 좌표 정보를 참고하여 프로젝트 데이터를 업데이트할 수 있습니다.

## 사용 방법

1. 대시보드에서 "GIS 지도" 메뉴를 클릭합니다.
2. 지도에서 프로젝트 마커를 클릭하면 상세 정보가 표시됩니다.
3. 필터 패널에서 카테고리와 상태별로 필터링할 수 있습니다.
4. 검색창에서 사업명이나 국가로 검색할 수 있습니다.

## 내부망 환경 고려사항

### 타일 맵 (지도 배경)

현재 구현에서는 타일 맵(지도 배경)이 없어도 마커는 정상적으로 표시됩니다. 

타일 맵이 필요한 경우:
1. 로컬 타일 서버 구축
2. 또는 간단한 지도 타일을 로컬에 저장

### 국기 이미지

국기 이미지는 현재 사용하지 않지만, 필요시 `frontend/images/flags/` 디렉토리에 저장할 수 있습니다.

## API 엔드포인트

- `GET /api/gis/projects` - GIS 프로젝트 데이터 조회
- `GET /api/gis/stats` - GIS 통계 조회
- `PUT /api/gis/projects/<id>/location` - 프로젝트 위치 업데이트

## 문제 해결

### 지도가 표시되지 않는 경우

1. Leaflet 라이브러리가 올바르게 다운로드되었는지 확인
2. 브라우저 콘솔에서 오류 메시지 확인
3. 네트워크 탭에서 파일 로드 상태 확인

### 마커가 표시되지 않는 경우

1. 프로젝트 데이터에 `latitude`와 `longitude` 값이 있는지 확인
2. 백엔드 API가 정상적으로 응답하는지 확인
3. 필터 설정이 모든 프로젝트를 숨기고 있지 않은지 확인

## 추가 개발

원본 KRC 지도의 고급 기능(타임라인, 국가별 통계 등)을 추가하려면 `frontend/gis.html` 파일을 수정하세요.


