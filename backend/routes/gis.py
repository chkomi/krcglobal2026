"""
GBMS - GIS Routes
글로벌사업처 해외사업관리시스템 - GIS 지도 API
"""
from flask import Blueprint, request, jsonify
from models import db, Project, ConsultingProject
from routes.auth import token_required

gis_bp = Blueprint('gis', __name__)


@gis_bp.route('/projects', methods=['GET'])
# @token_required  # 임시로 인증 비활성화 (개발용)
def get_gis_projects():
    """Get all projects with GIS data for map display (includes both regular and consulting projects)"""
    # Get query parameters
    project_type = request.args.get('type')
    category = request.args.get('category')  # 'consulting' or 'oda'
    country = request.args.get('country')
    status = request.args.get('status')
    search = request.args.get('search')
    include_consulting = request.args.get('includeConsulting', 'true').lower() == 'true'

    gis_projects = []

    # Get regular projects
    try:
        query = Project.query.filter(
            Project.latitude.isnot(None),
            Project.longitude.isnot(None),
            Project.latitude != 0,
            Project.longitude != 0
        )
    except Exception as e:
        print(f"좌표 필드 확인 실패: {e}")
        query = Project.query

    if project_type:
        query = query.filter(Project.project_type == project_type)

    if category:
        if category == 'consulting':
            query = query.filter(Project.project_type == 'consulting')
        elif category == 'oda':
            query = query.filter(Project.project_type.in_(['oda_bilateral', 'oda_multilateral']))

    if country:
        query = query.filter(Project.country == country)

    if status:
        query = query.filter(Project.status == status)

    if search:
        query = query.filter(
            db.or_(
                Project.title.ilike(f'%{search}%'),
                Project.code.ilike(f'%{search}%'),
                Project.country.ilike(f'%{search}%')
            )
        )

    projects = query.all()
    print(f"GIS API: 일반 프로젝트 {len(projects)}개 발견")

    # Transform regular projects to GIS format
    for project in projects:
        try:
            lat = float(project.latitude) if project.latitude else None
            lng = float(project.longitude) if project.longitude else None
        except (AttributeError, TypeError):
            continue

        if not lat or not lng or lat == 0 or lng == 0:
            continue

        cat = 'Consulting'
        if project.project_type in ['oda_bilateral', 'oda_multilateral']:
            cat = 'ODA'

        period = ''
        if project.start_date and project.end_date:
            period = f"'{project.start_date.year % 100}-'{project.end_date.year % 100}"
        elif project.start_date:
            period = f"'{project.start_date.year % 100}-"

        budget = float(project.budget_total) if project.budget_total else 0

        gis_project = {
            '__id': f'PROJECT-{project.id}',
            'source': 'regular',
            'name': project.country,
            'latitude': lat,
            'longitude': lng,
            'lat': lat,
            'lng': lng,
            'title': project.title,
            'description': project.title,
            'category': cat,
            'period': period,
            'budget': budget,
            'continent': project.region or '',
            'type': project.project_type,
            'status': project.status,
            'client': project.client or '',
            'startDate': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'endDate': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'budgetTotal': budget,
            'code': project.code
        }
        gis_projects.append(gis_project)

    # Get consulting projects
    if include_consulting:
        consulting_query = ConsultingProject.query.filter(
            ConsultingProject.latitude.isnot(None),
            ConsultingProject.longitude.isnot(None),
            ConsultingProject.latitude != 0,
            ConsultingProject.longitude != 0
        )

        if country:
            consulting_query = consulting_query.filter(ConsultingProject.country == country)

        if status:
            consulting_query = consulting_query.filter(ConsultingProject.status == status)

        if search:
            consulting_query = consulting_query.filter(
                db.or_(
                    ConsultingProject.title_kr.ilike(f'%{search}%'),
                    ConsultingProject.title_en.ilike(f'%{search}%'),
                    ConsultingProject.country.ilike(f'%{search}%')
                )
            )

        consulting_projects = consulting_query.all()
        print(f"GIS API: 해외기술용역 프로젝트 {len(consulting_projects)}개 발견")

        # Transform consulting projects to GIS format
        for cp in consulting_projects:
            try:
                lat = float(cp.latitude) if cp.latitude else None
                lng = float(cp.longitude) if cp.longitude else None
            except (AttributeError, TypeError):
                continue

            if not lat or not lng or lat == 0 or lng == 0:
                continue

            gis_project = {
                '__id': f'CONSULTING-{cp.id}',
                'source': 'consulting',
                'name': cp.country,
                'latitude': lat,
                'longitude': lng,
                'lat': lat,
                'lng': lng,
                'title': cp.title_kr,
                'titleEn': cp.title_en,
                'description': cp.title_kr,
                'category': 'Consulting',
                'period': f"{cp.start_date or ''}-{cp.end_date or ''}",
                'budget': float(cp.budget) if cp.budget else 0,
                'continent': '',
                'type': cp.project_type or '해외기술용역',
                'status': cp.status,
                'client': cp.client or '',
                'startDate': cp.start_date,
                'endDate': cp.end_date,
                'budgetTotal': float(cp.budget) if cp.budget else 0,
                'contractYear': cp.contract_year,
                'number': cp.number
            }
            gis_projects.append(gis_project)

    print(f"GIS API: 총 {len(gis_projects)}개의 프로젝트를 반환합니다.")

    return jsonify({
        'success': True,
        'data': gis_projects,
        'count': len(gis_projects)
    })


@gis_bp.route('/stats', methods=['GET'])
# @token_required  # 임시로 인증 비활성화 (개발용)
def get_gis_stats():
    """Get GIS statistics for map (includes consulting projects)"""
    # Count regular projects by category
    regular_consulting_count = Project.query.filter(
        Project.project_type == 'consulting',
        Project.latitude.isnot(None),
        Project.longitude.isnot(None)
    ).count()

    oda_count = Project.query.filter(
        Project.project_type.in_(['oda_bilateral', 'oda_multilateral']),
        Project.latitude.isnot(None),
        Project.longitude.isnot(None)
    ).count()

    # Count consulting projects
    consulting_projects_count = ConsultingProject.query.filter(
        ConsultingProject.latitude.isnot(None),
        ConsultingProject.longitude.isnot(None)
    ).count()

    # Total consulting = regular consulting + consulting projects
    total_consulting = regular_consulting_count + consulting_projects_count

    # Count by country from regular projects
    regular_country_stats = db.session.query(
        Project.country,
        db.func.count(Project.id)
    ).filter(
        Project.latitude.isnot(None),
        Project.longitude.isnot(None)
    ).group_by(Project.country).all()

    # Count by country from consulting projects
    consulting_country_stats = db.session.query(
        ConsultingProject.country,
        db.func.count(ConsultingProject.id)
    ).filter(
        ConsultingProject.latitude.isnot(None),
        ConsultingProject.longitude.isnot(None)
    ).group_by(ConsultingProject.country).all()

    # Merge country statistics
    country_dict = {}
    for country, count in regular_country_stats:
        country_dict[country] = country_dict.get(country, 0) + count
    for country, count in consulting_country_stats:
        country_dict[country] = country_dict.get(country, 0) + count

    return jsonify({
        'success': True,
        'data': {
            'consulting': total_consulting,
            'oda': oda_count,
            'total': total_consulting + oda_count,
            'consultingProjects': consulting_projects_count,
            'regularConsulting': regular_consulting_count,
            'byCountry': country_dict
        }
    })


@gis_bp.route('/projects/<int:project_id>/location', methods=['PUT'])
# @token_required  # 임시로 인증 비활성화 (개발용)
def update_project_location(project_id):
    """Update project location coordinates"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    if 'latitude' in data:
        project.latitude = data['latitude']
    if 'longitude' in data:
        project.longitude = data['longitude']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '위치 정보가 업데이트되었습니다.',
        'data': {
            'latitude': float(project.latitude) if project.latitude else None,
            'longitude': float(project.longitude) if project.longitude else None
        }
    })


