"""
GBMS - Dashboard Routes
글로벌사업처 해외사업관리시스템 - 대시보드 API
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, Project, Budget, Document, Office
from routes.auth import token_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/overview', methods=['GET'])
@token_required
def get_overview(current_user):
    """Get dashboard overview statistics"""
    current_year = datetime.now().year
    
    # Project statistics
    total_projects = Project.query.count()
    projects_in_progress = Project.query.filter(Project.status == 'in_progress').count()
    projects_completed = Project.query.filter(Project.status == 'completed').count()
    projects_planning = Project.query.filter(Project.status == 'planning').count()
    
    # Unique countries
    countries = db.session.query(Project.country).distinct().count()
    
    # Offices
    offices = Office.query.filter(Office.status == 'active').count()
    
    # Total budget
    total_budget = db.session.query(db.func.sum(Project.budget_total)).scalar() or 0
    
    # Budget execution (current year)
    total_planned = db.session.query(db.func.sum(Budget.amount_planned)).filter(
        Budget.year == current_year
    ).scalar() or 0
    total_executed = db.session.query(db.func.sum(Budget.amount_executed)).filter(
        Budget.year == current_year
    ).scalar() or 0
    
    execution_rate = round(float(total_executed) / float(total_planned) * 100, 1) if total_planned else 0
    
    # Projects by type
    by_type = db.session.query(
        Project.project_type,
        db.func.count(Project.id)
    ).filter(Project.status.in_(['in_progress', 'planning'])).group_by(Project.project_type).all()
    
    # Projects by department  
    by_department = db.session.query(
        Project.department,
        db.func.count(Project.id)
    ).filter(Project.status.in_(['in_progress', 'planning'])).group_by(Project.department).all()
    
    return jsonify({
        'success': True,
        'data': {
            'projects': {
                'total': total_projects,
                'inProgress': projects_in_progress,
                'completed': projects_completed,
                'planning': projects_planning
            },
            'countries': countries,
            'offices': offices,
            'budget': {
                'total': float(total_budget),
                'planned': float(total_planned),
                'executed': float(total_executed),
                'executionRate': execution_rate
            },
            'byType': {t[0]: t[1] for t in by_type},
            'byDepartment': {d[0]: d[1] for d in by_department}
        }
    })


@dashboard_bp.route('/recent-projects', methods=['GET'])
@token_required
def get_recent_projects(current_user):
    """Get recent projects for dashboard"""
    limit = request.args.get('limit', 5, type=int)
    
    projects = Project.query.order_by(
        Project.updated_at.desc()
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': [p.to_dict() for p in projects]
    })


@dashboard_bp.route('/department-budgets', methods=['GET'])
@token_required
def get_department_budgets(current_user):
    """Get budget by department for current year"""
    current_year = datetime.now().year
    
    dept_names = {
        'gad': '글로벌농업개발부',
        'gb': '글로벌사업부',
        'aidc': '농식품국제개발협력센터'
    }
    
    budgets = db.session.query(
        Project.department,
        db.func.sum(Budget.amount_planned).label('planned'),
        db.func.sum(Budget.amount_executed).label('executed')
    ).join(Project).filter(
        Budget.year == current_year
    ).group_by(Project.department).all()
    
    result = []
    for b in budgets:
        planned = float(b.planned) if b.planned else 0
        executed = float(b.executed) if b.executed else 0
        result.append({
            'department': b.department,
            'departmentName': dept_names.get(b.department, b.department),
            'planned': planned,
            'executed': executed,
            'rate': round(executed / planned * 100, 1) if planned else 0
        })
    
    return jsonify({
        'success': True,
        'data': result
    })


@dashboard_bp.route('/country-stats', methods=['GET'])
@token_required
def get_country_stats(current_user):
    """Get project statistics by country"""
    countries = db.session.query(
        Project.country,
        Project.country_code,
        Project.region,
        db.func.count(Project.id).label('project_count'),
        db.func.sum(Project.budget_total).label('total_budget')
    ).group_by(
        Project.country, Project.country_code, Project.region
    ).order_by(
        db.func.count(Project.id).desc()
    ).all()
    
    return jsonify({
        'success': True,
        'data': [
            {
                'country': c.country,
                'countryCode': c.country_code,
                'region': c.region,
                'projectCount': c.project_count,
                'totalBudget': float(c.total_budget) if c.total_budget else 0
            }
            for c in countries
        ]
    })


@dashboard_bp.route('/upcoming-events', methods=['GET'])
@token_required
def get_upcoming_events(current_user):
    """Get upcoming events/deadlines"""
    limit = request.args.get('limit', 5, type=int)
    today = datetime.now().date()
    
    # Projects with upcoming end dates
    upcoming_projects = Project.query.filter(
        Project.end_date >= today,
        Project.status == 'in_progress'
    ).order_by(Project.end_date).limit(limit).all()
    
    events = []
    for p in upcoming_projects:
        events.append({
            'type': 'project_deadline',
            'date': p.end_date.isoformat() if p.end_date else None,
            'title': f'{p.title} 종료',
            'description': p.country,
            'department': p.department
        })
    
    return jsonify({
        'success': True,
        'data': events
    })


@dashboard_bp.route('/activity-log', methods=['GET'])
@token_required
def get_activity_log(current_user):
    """Get recent activity log"""
    from models import ActivityLog
    
    limit = request.args.get('limit', 10, type=int)
    
    logs = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': [log.to_dict() for log in logs]
    })
