#!/bin/bash
# Leaflet 라이브러리 다운로드 스크립트
# 내부망 환경에서 사용할 수 있도록 로컬에 다운로드

echo "Leaflet 라이브러리 다운로드 중..."

# 디렉토리 생성
mkdir -p frontend/lib/leaflet

# Leaflet CSS 다운로드
echo "CSS 다운로드 중..."
curl -L -o frontend/lib/leaflet/leaflet.css "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" || echo "CSS 다운로드 실패"

# Leaflet JS 다운로드
echo "JS 다운로드 중..."
curl -L -o frontend/lib/leaflet/leaflet.js "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" || echo "JS 다운로드 실패"

# Leaflet 이미지 파일들 다운로드
echo "이미지 파일 다운로드 중..."
mkdir -p frontend/lib/leaflet/images

# 마커 아이콘 이미지들
curl -L -o frontend/lib/leaflet/images/marker-icon.png "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png" || echo "marker-icon.png 다운로드 실패"
curl -L -o frontend/lib/leaflet/images/marker-icon-2x.png "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png" || echo "marker-icon-2x.png 다운로드 실패"
curl -L -o frontend/lib/leaflet/images/marker-shadow.png "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png" || echo "marker-shadow.png 다운로드 실패"

echo "다운로드 완료!"
echo "참고: 내부망 환경에서는 인터넷 연결이 필요합니다."
echo "인터넷이 없는 경우, 외부에서 다운로드한 파일을 frontend/lib/leaflet/ 디렉토리에 복사하세요."


