# CORS 문제 해결 가이드

## 문제 상황

```
Access to fetch at 'http://127.0.0.1:5000/api/gis/projects' from origin 'http://127.0.0.1:5500' 
has been blocked by CORS policy
```

이 오류는 브라우저의 보안 정책 때문에 발생합니다. 다른 포트(5500)에서 실행 중인 페이지가 다른 포트(5000)의 API를 호출할 때 CORS 설정이 필요합니다.

## 해결 방법

### 방법 1: Flask 서버에서 직접 프론트엔드 제공 (권장)

정적 파일 서버(Live Server)를 사용하지 않고 Flask 서버에서 직접 프론트엔드를 제공:

1. **Flask 서버 실행:**
   ```bash
   cd backend
   python app.py
   ```

2. **브라우저에서 접속:**
   ```
   http://127.0.0.1:5000/gis.html
   ```

이 경우 CORS 문제가 발생하지 않습니다.

### 방법 2: CORS 설정 확인

Flask 서버가 실행 중인지 확인하고, CORS 설정이 올바른지 확인:

1. **Flask 서버 실행 확인:**
   ```bash
   cd backend
   python app.py
   ```

2. **CORS 설정 확인:**
   - `backend/app.py`에서 CORS 설정 확인
   - 현재 모든 origin을 허용하도록 설정됨

3. **브라우저에서 테스트:**
   ```
   http://127.0.0.1:5000/api/health
   ```
   정상 응답이 오는지 확인

### 방법 3: 브라우저 CORS 확장 프로그램 사용 (개발용)

Chrome 확장 프로그램 "CORS Unblock" 등을 사용하여 개발 중에만 CORS를 우회할 수 있습니다. (프로덕션에서는 사용하지 마세요)

## 현재 설정

코드에서 CORS를 다음과 같이 설정했습니다:

```python
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

이 설정으로 모든 origin에서 API에 접근할 수 있습니다.

## 확인 방법

1. **Flask 서버가 실행 중인지 확인:**
   ```bash
   # 터미널에서 확인
   curl http://127.0.0.1:5000/api/health
   ```

2. **브라우저에서 직접 테스트:**
   ```
   http://127.0.0.1:5000/api/gis/projects
   ```

3. **Network 탭 확인:**
   - OPTIONS 요청이 200 OK로 응답하는지 확인
   - GET 요청이 정상적으로 처리되는지 확인

## 추가 문제 해결

### Flask 서버가 실행되지 않는 경우

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 포트 충돌

다른 프로그램이 포트 5000을 사용 중인 경우:
- 포트를 변경하거나
- 해당 프로그램을 종료

### 데이터베이스 오류

```bash
cd backend
python init_db.py
```

