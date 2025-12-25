"""
GBMS - Flask Application Entry Point
글로벌사업처 해외사업관리시스템
"""
import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from config import config

# Create Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load configuration
config_name = os.environ.get('FLASK_ENV') or 'development'
app.config.from_object(config[config_name])

# Enable CORS for internal network
# 개발 환경: 모든 origin 허용
CORS(app, 
     resources={r"/*": {"origins": "*"}},  # 모든 경로에 CORS 적용
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type"])

# OPTIONS 요청 전역 처리
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,X-Requested-With")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        response.headers.add('Access-Control-Max-Age', "3600")
        return response

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)

# Initialize database
from models import db
db.init_app(app)

# Enable WAL mode for SQLite (better concurrent access)
def setup_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Enable WAL mode for better concurrent write performance
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            try:
                from sqlalchemy import text
                with db.engine.connect() as conn:
                    conn.execute(text('PRAGMA journal_mode=WAL'))
                    conn.execute(text('PRAGMA synchronous=NORMAL'))
                    conn.execute(text('PRAGMA cache_size=-64000'))  # 64MB cache
                    conn.execute(text('PRAGMA busy_timeout=30000'))  # 30s timeout
                    conn.commit()
            except Exception as e:
                print(f"SQLite 설정 오류 (무시 가능): {e}")

# 앱 시작 시 데이터베이스 설정
with app.app_context():
    setup_database()


# Register blueprints (API routes)
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.budgets import budgets_bp
from routes.documents import documents_bp
from routes.dashboard import dashboard_bp
from routes.users import users_bp
from routes.offices import offices_bp
from routes.gis import gis_bp
from routes.consulting import consulting_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
app.register_blueprint(documents_bp, url_prefix='/api/documents')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(offices_bp, url_prefix='/api/offices')
app.register_blueprint(gis_bp, url_prefix='/api/gis')
app.register_blueprint(consulting_bp, url_prefix='/api/consulting')


# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': '요청한 리소스를 찾을 수 없습니다.'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': '서버 내부 오류가 발생했습니다.'}), 500


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': '파일 크기가 너무 큽니다. 최대 50MB까지 업로드 가능합니다.'}), 413


# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'GBMS',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    # Run the Flask development server
    # In production, use a WSGI server like gunicorn
    app.run(
        host='0.0.0.0',  # Allow connections from other machines in the network
        port=5001,
        debug=app.config['DEBUG']
    )
