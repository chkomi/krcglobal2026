# Leaflet 라이브러리 수동 다운로드 가이드

## 내부망 환경용 설치 가이드

외부 인터넷이 연결되지 않은 내부망 환경에서 Leaflet 라이브러리를 설치하는 방법입니다.

## 필요한 파일 목록

다음 5개 파일을 외부 인터넷이 연결된 환경에서 다운로드하세요:

### 1. CSS 파일
- **파일명**: `leaflet.css`
- **다운로드 URL**: https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
- **저장 위치**: `frontend/lib/leaflet/leaflet.css`

### 2. JavaScript 파일
- **파일명**: `leaflet.js`
- **다운로드 URL**: https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
- **저장 위치**: `frontend/lib/leaflet/leaflet.js`

### 3. 이미지 파일 (3개)
다음 3개 이미지 파일을 `frontend/lib/leaflet/images/` 디렉토리에 저장하세요:

- **marker-icon.png**
  - URL: https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
  - 저장 위치: `frontend/lib/leaflet/images/marker-icon.png`

- **marker-icon-2x.png**
  - URL: https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
  - 저장 위치: `frontend/lib/leaflet/images/marker-icon-2x.png`

- **marker-shadow.png**
  - URL: https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png
  - 저장 위치: `frontend/lib/leaflet/images/marker-shadow.png`

## 다운로드 방법

### 방법 1: 브라우저에서 직접 다운로드 (가장 간단) ⭐ 권장

**외부 인터넷이 연결된 컴퓨터에서:**

1. 브라우저(Chrome, Edge, Firefox 등)를 엽니다.
2. 아래 URL들을 하나씩 주소창에 입력하거나 클릭합니다.
3. 각 URL을 열면 파일이 자동으로 다운로드됩니다.
4. 다운로드된 파일들을 ZIP으로 압축하여 메일로 전송합니다.

**다운로드할 URL 목록:**

```
1. https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
2. https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
3. https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
4. https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
5. https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png
```

**팁:** 
- 각 URL을 새 탭에서 열면 파일이 바로 다운로드됩니다.
- 다운로드 폴더에서 파일명을 확인하세요.
- 5개 파일을 모두 다운로드한 후 ZIP으로 압축하세요.

### 방법 2: curl 사용 (Mac/Linux에서 사용 가능한 경우)

```bash
# 디렉토리 생성
mkdir -p leaflet_files/images

# 파일 다운로드
curl -o leaflet_files/leaflet.css https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
curl -o leaflet_files/leaflet.js https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
curl -o leaflet_files/images/marker-icon.png https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png
curl -o leaflet_files/images/marker-icon-2x.png https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png
curl -o leaflet_files/images/marker-shadow.png https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png

# ZIP으로 압축
zip -r leaflet-1.9.4.zip leaflet_files/
```

### 방법 3: PowerShell 사용 (Windows)

Windows PowerShell에서:

```powershell
# 디렉토리 생성
New-Item -ItemType Directory -Force -Path leaflet_files\images

# 파일 다운로드
Invoke-WebRequest -Uri "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" -OutFile "leaflet_files\leaflet.css"
Invoke-WebRequest -Uri "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" -OutFile "leaflet_files\leaflet.js"
Invoke-WebRequest -Uri "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png" -OutFile "leaflet_files\images\marker-icon.png"
Invoke-WebRequest -Uri "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png" -OutFile "leaflet_files\images\marker-icon-2x.png"
Invoke-WebRequest -Uri "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png" -OutFile "leaflet_files\images\marker-shadow.png"

# ZIP으로 압축 (Windows 10 이상)
Compress-Archive -Path leaflet_files -DestinationPath leaflet-1.9.4.zip
```

## 설치 방법

### 1단계: 디렉토리 생성

내부망 컴퓨터에서 프로젝트 루트 디렉토리로 이동한 후:

```bash
mkdir -p frontend/lib/leaflet/images
```

### 2단계: 파일 복사

다운로드한 파일들을 다음 위치에 복사합니다:

```
프로젝트루트/
  frontend/
    lib/
      leaflet/
        leaflet.css          ← 여기에 복사
        leaflet.js           ← 여기에 복사
        images/
          marker-icon.png    ← 여기에 복사
          marker-icon-2x.png ← 여기에 복사
          marker-shadow.png  ← 여기에 복사
```

### 3단계: 파일 확인

다음 명령어로 파일이 올바르게 설치되었는지 확인합니다:

```bash
# Mac/Linux
ls -la frontend/lib/leaflet/
ls -la frontend/lib/leaflet/images/

# Windows (PowerShell)
dir frontend\lib\leaflet
dir frontend\lib\leaflet\images
```

## 최종 디렉토리 구조

설치가 완료되면 다음과 같은 구조가 되어야 합니다:

```
frontend/
  lib/
    leaflet/
      ├── leaflet.css
      ├── leaflet.js
      └── images/
          ├── marker-icon.png
          ├── marker-icon-2x.png
          └── marker-shadow.png
```

## 검증

설치가 완료된 후 브라우저에서 `gis.html` 페이지를 열어서:

1. 브라우저 개발자 도구(F12)를 엽니다.
2. Console 탭에서 오류가 없는지 확인합니다.
3. Network 탭에서 `leaflet.css`와 `leaflet.js` 파일이 정상적으로 로드되는지 확인합니다.

## 문제 해결

### 파일을 찾을 수 없다는 오류가 발생하는 경우

1. 파일 경로가 정확한지 확인하세요.
2. 파일명이 정확한지 확인하세요 (대소문자 구분).
3. 브라우저 콘솔에서 실제 요청 경로를 확인하세요.

### 이미지가 표시되지 않는 경우

1. `images/` 디렉토리가 올바른 위치에 있는지 확인하세요.
2. 이미지 파일명이 정확한지 확인하세요.
3. Leaflet CSS 파일에서 이미지 경로가 `images/`로 설정되어 있는지 확인하세요.

## 참고사항

- Leaflet 버전: 1.9.4 (안정 버전)
- 파일 총 크기: 약 200KB (압축 시)
- 타일 맵(지도 배경)은 별도로 필요하지 않습니다. 마커만 표시해도 정상 작동합니다.

