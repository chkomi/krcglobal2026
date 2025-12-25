# GIS API 데이터 소스 설명

## 데이터 흐름

```
SQLite 데이터베이스 → Project 모델 → GIS API → 프론트엔드 지도
```

## 1. 데이터 소스: SQLite 데이터베이스

**위치**: `backend/database/` 디렉토리
**파일명**: `gbms.db` (또는 config.py에 설정된 이름)

데이터베이스에는 `projects` 테이블이 있고, 여기에 모든 프로젝트 정보가 저장됩니다.

## 2. 데이터 모델: Project

**파일**: `backend/models/__init__.py`

Project 모델의 주요 필드:
- `id`: 프로젝트 ID
- `code`: 사업 코드
- `title`: 사업명
- `country`: 국가
- `latitude`: 위도 (GIS용)
- `longitude`: 경도 (GIS용)
- `project_type`: 사업 유형 (consulting, oda_bilateral, oda_multilateral 등)
- `status`: 상태 (planning, in_progress, completed 등)
- `budget_total`: 총 예산
- `start_date`, `end_date`: 기간
- 기타...

## 3. GIS API 엔드포인트

**파일**: `backend/routes/gis.py`
**엔드포인트**: `GET /api/gis/projects`

### 동작 방식:

1. **데이터베이스 쿼리**:
   ```python
   Project.query.filter(
       Project.latitude.isnot(None),
       Project.longitude.isnot(None),
       Project.latitude != 0,
       Project.longitude != 0
   )
   ```
   - 좌표(`latitude`, `longitude`)가 있는 프로젝트만 조회
   - 좌표가 0이 아닌 프로젝트만 포함

2. **데이터 변환**:
   - 데이터베이스의 Project 객체를 GIS 형식으로 변환
   - KRC 지도 형식과 호환되도록 변환

3. **응답 반환**:
   ```json
   {
     "success": true,
     "data": [
       {
         "name": "베트남",
         "lat": 14.0583,
         "lng": 108.2772,
         "description": "사업명",
         "category": "ODA",
         ...
       }
     ],
     "count": 5
   }
   ```

## 4. 프론트엔드에서 사용

**파일**: `frontend/gis.html`, `frontend/js/api.js`

```javascript
// API 호출
const response = await API.get('/gis/projects');

// 데이터 변환
allProjects = response.data.map(project => ({
    ...project,
    lat: project.latitude,
    lng: project.longitude,
    ...
}));

// 마커 생성
filteredProjects.forEach(project => {
    const marker = createMarker(project);
    markersLayer.addLayer(marker);
});
```

## 데이터가 없는 경우

현재 데이터베이스에 프로젝트가 없거나, 좌표 정보가 없는 경우:

1. **데이터베이스 초기화**:
   ```bash
   cd backend
   python init_db.py
   ```

2. **프로젝트 데이터 추가**:
   - 관리자 페이지에서 프로젝트 등록
   - 또는 KRC JSON 파일에서 데이터 가져오기
   - 또는 직접 데이터베이스에 입력

3. **좌표 정보 추가**:
   - 프로젝트 등록 시 `latitude`, `longitude` 입력
   - 또는 KRC JSON 파일의 좌표 정보 활용

## KRC 데이터 활용

KRC 레포지토리의 JSON 파일(`KRC/data/global_oda.json`, `global_consulting.json`)에서 좌표 정보를 가져와서 데이터베이스에 추가할 수 있습니다.

### 예시 스크립트:

```python
from app import app, db
from models import Project
import json

with app.app_context():
    # KRC JSON 파일 읽기
    with open('KRC/data/global_oda.json', 'r', encoding='utf-8') as f:
        oda_data = json.load(f)
    
    # 프로젝트 업데이트 또는 생성
    for item in oda_data:
        project = Project.query.filter_by(
            country=item['name'],
            title=item['description']
        ).first()
        
        if project:
            # 기존 프로젝트에 좌표 추가
            project.latitude = item['lat']
            project.longitude = item['lng']
        else:
            # 새 프로젝트 생성
            project = Project(
                code=f"ODA-{item.get('number', 'UNK')}",
                title=item['description'],
                country=item['name'],
                latitude=item['lat'],
                longitude=item['lng'],
                project_type='oda_bilateral',
                department='aidc',
                budget_total=item.get('budget', 0) * 1000000,  # 백만원 단위
                status='in_progress'
            )
            db.session.add(project)
    
    db.session.commit()
```

## 요약

- **데이터 소스**: SQLite 데이터베이스 (`backend/database/`)
- **데이터 모델**: `Project` 모델 (`backend/models/__init__.py`)
- **API 엔드포인트**: `GET /api/gis/projects` (`backend/routes/gis.py`)
- **데이터 형식**: JSON (GIS 지도 형식으로 변환)
- **필수 조건**: 프로젝트에 `latitude`와 `longitude` 값이 있어야 함

