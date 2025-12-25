"""
GBMS - Authentication Routes
글로벌사업처 해외사업관리시스템
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import jwt
from functools import wraps
from models import db, User, ActivityLog

auth_bp = Blueprint('auth', __name__)


def get_secret_key():
    from flask import current_app
    return current_app.config['JWT_SECRET_KEY']


def token_required(f):
    """JWT token verification decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': '유효하지 않은 토큰 형식입니다.'}), 401
        
        if not token:
            return jsonify({'message': '인증 토큰이 필요합니다.'}), 401
        
        try:
            data = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'message': '사용자를 찾을 수 없습니다.'}), 401
            
            if not current_user.is_active:
                return jsonify({'message': '비활성화된 계정입니다.'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '토큰이 만료되었습니다.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '유효하지 않은 토큰입니다.'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """Admin role verification decorator"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': '관리자 권한이 필요합니다.'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '요청 데이터가 없습니다.'}), 400
    
    user_id = data.get('userId')
    password = data.get('password')
    
    if not user_id or not password:
        return jsonify({'success': False, 'message': '아이디와 비밀번호를 입력해주세요.'}), 400
    
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}), 401
    
    if not user.is_active:
        return jsonify({'success': False, 'message': '비활성화된 계정입니다. 관리자에게 문의하세요.'}), 401
    
    # Generate JWT token
    from flask import current_app
    token_expires = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + token_expires
    }, get_secret_key(), algorithm='HS256')
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Log activity
    log = ActivityLog(
        user_id=user.id,
        action='login',
        entity_type='user',
        entity_id=user.id,
        description=f'{user.name}님이 로그인했습니다.',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'token': token,
        'user': user.to_dict()
    })


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout"""
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='logout',
        entity_type='user',
        entity_id=current_user.id,
        description=f'{current_user.name}님이 로그아웃했습니다.',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '로그아웃되었습니다.'})


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user info"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })


@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change password"""
    data = request.get_json()
    
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    if not current_password or not new_password:
        return jsonify({'success': False, 'message': '현재 비밀번호와 새 비밀번호를 입력해주세요.'}), 400
    
    if not current_user.check_password(current_password):
        return jsonify({'success': False, 'message': '현재 비밀번호가 올바르지 않습니다.'}), 400
    
    if len(new_password) < 6:
        return jsonify({'success': False, 'message': '새 비밀번호는 6자 이상이어야 합니다.'}), 400
    
    current_user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '비밀번호가 변경되었습니다.'})
