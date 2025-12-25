"""
GBMS - Users Routes
글로벌사업처 해외사업관리시스템 - 사용자관리 API
"""
from flask import Blueprint, request, jsonify
from models import db, User, ActivityLog
from routes.auth import token_required, admin_required

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@token_required
def get_users(current_user):
    """Get all users"""
    department = request.args.get('department')
    is_active = request.args.get('is_active', type=bool)
    
    query = User.query
    
    if department:
        query = query.filter(User.department == department)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    users = query.order_by(User.name).all()
    
    return jsonify({
        'success': True,
        'data': [u.to_dict() for u in users]
    })


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """Get single user by ID"""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    })


@users_bp.route('', methods=['POST'])
@admin_required
def create_user(current_user):
    """Create new user (admin only)"""
    data = request.get_json()
    
    required_fields = ['userId', 'name', 'department', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} 필드는 필수입니다.'}), 400
    
    # Check for duplicate user_id
    if User.query.filter_by(user_id=data['userId']).first():
        return jsonify({'success': False, 'message': '이미 존재하는 사번/아이디입니다.'}), 400
    
    user = User(
        user_id=data['userId'],
        name=data['name'],
        email=data.get('email'),
        department=data['department'],
        role=data.get('role', 'user'),
        phone=data.get('phone'),
        position=data.get('position'),
        is_active=data.get('isActive', True)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '사용자가 등록되었습니다.',
        'data': user.to_dict()
    }), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(current_user, user_id):
    """Update user (admin only)"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'department' in data:
        user.department = data['department']
    if 'role' in data:
        user.role = data['role']
    if 'phone' in data:
        user.phone = data['phone']
    if 'position' in data:
        user.position = data['position']
    if 'isActive' in data:
        user.is_active = data['isActive']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '사용자 정보가 수정되었습니다.',
        'data': user.to_dict()
    })


@users_bp.route('/<int:user_id>/password', methods=['PUT'])
@admin_required
def reset_password(current_user, user_id):
    """Reset user password (admin only)"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data.get('newPassword'):
        return jsonify({'success': False, 'message': '새 비밀번호를 입력해주세요.'}), 400
    
    user.set_password(data['newPassword'])
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '비밀번호가 초기화되었습니다.'
    })


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    """Delete user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': '자기 자신은 삭제할 수 없습니다.'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '사용자가 삭제되었습니다.'
    })
