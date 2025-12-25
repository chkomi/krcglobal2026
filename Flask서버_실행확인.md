# Flask 서버 실행 확인 가이드

## CORS 오류 해결

CORS 오류가 발생하는 경우 Flask 서버가 제대로 실행되지 않았을 수 있습니다.

## 1단계: Flask 서버 실행 확인

### 서버가 실행 중인지 확인:

터미널에서 다음 명령어로 확인:

```bash
# 포트 5000이 사용 중인지 확인
lsof -i :5000

# 또는
netstat -an | grep 5000
```

### 서버 실행:

```bash
cd backend
python app.py
```

**정상 실행 시 출력:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## 2단계: 서버 응답 확인

브라우저에서 직접 테스트:

```
http://127.0.0.1:5000/api/health
```

**정상 응답:**
```json
{
  "status": "healthy",
  "service": "GBMS",
  "version": "1.0.0"
}
```

## 3단계: GIS API 직접 테스트

```
http://127.0.0.1:5000/api/gis/projects
```

**정상 응답:**
```json
{
  "success": true,
  "data": [...],
  "count": 0
}
```

## 4단계: CORS 헤더 확인

브라우저 개발자 도구(F12) → Network 탭:
1. `/api/gis/projects` 요청 선택
2. Response Headers 확인:
   - `Access-Control-Allow-Origin: *` 있어야 함

## 문제 해결

### 문제 1: "Connection refused"

**원인**: Flask 서버가 실행되지 않음
**해결**: `cd backend && python app.py` 실행

### 문제 2: "ModuleNotFoundError: No module named 'flask'"

**원인**: Flask가 설치되지 않음
**해결**: 
```bash
cd backend
pip install -r requirements.txt
```

### 문제 3: CORS 오류가 계속 발생

**해결 방법 A**: Flask 서버에서 직접 접속 (권장)
```
http://127.0.0.1:5000/gis.html
```

**해결 방법 B**: 서버 재시작
1. Flask 서버 중지 (Ctrl+C)
2. 서버 재시작: `python app.py`
3. 브라우저 새로고침

## 빠른 테스트

터미널에서:

```bash
# 1. Flask 서버 실행
cd backend
python app.py

# 2. 다른 터미널에서 테스트
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/gis/projects
```

정상 응답이 오면 서버는 정상 작동 중입니다.

