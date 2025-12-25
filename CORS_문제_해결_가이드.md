# CORS 문제 해결 가이드

## 문제 상황
브라우저에서 `http://127.0.0.1:5500` (Live Server)로 접속하면 Flask 서버(`http://127.0.0.1:5000`)로의 요청이 CORS 오류로 차단됩니다.

## 해결 방법 (2가지)

### 방법 1: Flask 서버에서 직접 접속 (권장) ⭐

**CORS 문제가 전혀 발생하지 않습니다!**

1. **Flask 서버 실행:**
   ```bash
   cd backend
   python app.py
   ```

2. **브라우저에서 접속:**
   ```
   http://127.0.0.1:5000/gis.html
   ```

3. **장점:**
   - CORS 문제 없음
   - 하나의 서버만 실행하면 됨
   - 프로덕션 환경과 유사

### 방법 2: Live Server 사용 (개발용)

Live Server를 계속 사용하려면 Flask 서버가 실행 중이어야 합니다.

1. **Flask 서버 실행:**
   ```bash
   cd backend
   python app.py
   ```

2. **서버가 정상 실행되었는지 확인:**
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
   
   정상 응답:
   ```json
   {"status":"healthy","service":"GBMS","version":"1.0.0"}
   ```

3. **브라우저에서 접속:**
   ```
   http://127.0.0.1:5500/frontend/gis.html
   ```

4. **여전히 CORS 오류가 발생하면:**
   - Flask 서버를 재시작하세요 (Ctrl+C 후 다시 실행)
   - 브라우저 캐시를 지우고 새로고침 (Ctrl+Shift+R)

## Flask 서버 실행 확인

### 서버가 실행 중인지 확인:

```bash
# 방법 1: 포트 확인
lsof -i :5000

# 방법 2: curl 테스트
curl http://127.0.0.1:5000/api/health

# 방법 3: 브라우저에서 직접 접속
http://127.0.0.1:5000/api/health
```

### 서버 실행 오류 해결:

**오류: `ModuleNotFoundError: No module named 'flask'`**
```bash
cd backend
pip install -r requirements.txt
```

**오류: `Address already in use`**
```bash
# 포트 5000을 사용하는 프로세스 종료
lsof -ti:5000 | xargs kill -9
```

## 권장 사항

**개발 중에는 방법 1 (Flask 서버 직접 접속)을 권장합니다:**
- CORS 문제 없음
- 설정 간단
- 프로덕션과 유사한 환경

**Live Server는 HTML/CSS/JS 수정 시 실시간 미리보기용으로만 사용하세요.**

