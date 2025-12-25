#!/bin/bash

# KRC Global 2026 시작 스크립트

echo "🌏 KRC Global 2026 해외사업관리시스템 시작"
echo "=========================================="
echo ""

# 백엔드 서버 확인
if [ -f "backend/app.py" ]; then
    echo "✅ 백엔드 서버 시작 중..."
    cd backend
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo "   백엔드 서버 PID: $BACKEND_PID"
    echo "   API 주소: http://localhost:5000"
else
    echo "⚠️  백엔드 서버를 찾을 수 없습니다."
fi

echo ""
echo "✅ 프론트엔드 서버 시작 중..."
python -m http.server 8000 &
FRONTEND_PID=$!
echo "   프론트엔드 서버 PID: $FRONTEND_PID"
echo "   웹 주소: http://localhost:8000"

echo ""
echo "=========================================="
echo "🎉 시스템이 시작되었습니다!"
echo ""
echo "📱 브라우저에서 접속하세요:"
echo "   http://localhost:8000/index.html"
echo ""
echo "⏹️  종료하려면 Ctrl+C를 누르세요"
echo "=========================================="

# 종료 시 프로세스 정리
trap "echo ''; echo '⏹️  서버를 종료합니다...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 대기
wait
