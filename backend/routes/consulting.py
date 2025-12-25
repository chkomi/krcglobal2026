"""
GBMS - Consulting Projects Routes
해외기술용역 프로젝트 관리 API
"""
from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from models import db, ConsultingProject, ActivityLog
from routes.auth import token_required

consulting_bp = Blueprint('consulting', __name__)


@consulting_bp.route('', methods=['GET'])
@token_required
def get_consulting_projects(current_user):
    """Get all consulting projects with filters"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    country = request.args.get('country')
    status = request.args.get('status')
    year = request.args.get('year', type=int)
    client = request.args.get('client')
    search = request.args.get('search')

    # Build query
    query = ConsultingProject.query

    if country:
        query = query.filter(ConsultingProject.country == country)

    if status:
        query = query.filter(ConsultingProject.status == status)

    if year:
        query = query.filter(ConsultingProject.contract_year == year)

    if client:
        query = query.filter(ConsultingProject.client.ilike(f'%{client}%'))

    if search:
        query = query.filter(
            db.or_(
                ConsultingProject.title_kr.ilike(f'%{search}%'),
                ConsultingProject.title_en.ilike(f'%{search}%'),
                ConsultingProject.country.ilike(f'%{search}%'),
                ConsultingProject.client.ilike(f'%{search}%')
            )
        )

    # Order by contract year (descending) and number
    query = query.order_by(
        ConsultingProject.contract_year.desc(),
        ConsultingProject.number.asc()
    )

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'success': True,
        'data': [project.to_dict() for project in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'currentPage': page
    })


@consulting_bp.route('/<int:project_id>', methods=['GET'])
@token_required
def get_consulting_project(current_user, project_id):
    """Get single consulting project"""
    project = ConsultingProject.query.get_or_404(project_id)

    return jsonify({
        'success': True,
        'data': project.to_dict()
    })


@consulting_bp.route('', methods=['POST'])
@token_required
def create_consulting_project(current_user):
    """Create new consulting project"""
    data = request.get_json()

    if not data or not data.get('titleKr') or not data.get('country'):
        return jsonify({
            'success': False,
            'message': '국문사업명과 국가는 필수 입력 항목입니다.'
        }), 400

    # Create new project
    project = ConsultingProject(
        number=data.get('number'),
        contract_year=data.get('contractYear'),
        status=data.get('status', '준공'),
        country=data.get('country'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        title_en=data.get('titleEn'),
        title_kr=data.get('titleKr'),
        project_type=data.get('projectType'),
        start_date=data.get('startDate'),
        end_date=data.get('endDate'),
        budget=data.get('budget'),
        client=data.get('client'),
        created_by=current_user.id
    )

    db.session.add(project)

    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='create',
        entity_type='consulting_project',
        entity_id=project.id,
        description=f'{current_user.name}님이 해외기술용역 프로젝트를 생성했습니다: {project.title_kr}',
        ip_address=request.remote_addr
    )
    db.session.add(log)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': '프로젝트가 생성되었습니다.',
        'data': project.to_dict()
    }), 201


@consulting_bp.route('/<int:project_id>', methods=['PUT'])
@token_required
def update_consulting_project(current_user, project_id):
    """Update consulting project"""
    project = ConsultingProject.query.get_or_404(project_id)
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': '수정할 데이터가 없습니다.'
        }), 400

    # Update fields
    if 'number' in data:
        project.number = data['number']
    if 'contractYear' in data:
        project.contract_year = data['contractYear']
    if 'status' in data:
        project.status = data['status']
    if 'country' in data:
        project.country = data['country']
    if 'latitude' in data:
        project.latitude = data['latitude']
    if 'longitude' in data:
        project.longitude = data['longitude']
    if 'titleEn' in data:
        project.title_en = data['titleEn']
    if 'titleKr' in data:
        project.title_kr = data['titleKr']
    if 'projectType' in data:
        project.project_type = data['projectType']
    if 'startDate' in data:
        project.start_date = data['startDate']
    if 'endDate' in data:
        project.end_date = data['endDate']
    if 'budget' in data:
        project.budget = data['budget']
    if 'client' in data:
        project.client = data['client']

    project.updated_at = datetime.utcnow()

    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='update',
        entity_type='consulting_project',
        entity_id=project.id,
        description=f'{current_user.name}님이 해외기술용역 프로젝트를 수정했습니다: {project.title_kr}',
        ip_address=request.remote_addr
    )
    db.session.add(log)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': '프로젝트가 수정되었습니다.',
        'data': project.to_dict()
    })


@consulting_bp.route('/<int:project_id>', methods=['DELETE'])
@token_required
def delete_consulting_project(current_user, project_id):
    """Delete consulting project"""
    project = ConsultingProject.query.get_or_404(project_id)

    project_title = project.title_kr

    # Log activity before deletion
    log = ActivityLog(
        user_id=current_user.id,
        action='delete',
        entity_type='consulting_project',
        entity_id=project.id,
        description=f'{current_user.name}님이 해외기술용역 프로젝트를 삭제했습니다: {project_title}',
        ip_address=request.remote_addr
    )
    db.session.add(log)

    db.session.delete(project)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '프로젝트가 삭제되었습니다.'
    })


@consulting_bp.route('/export', methods=['GET'])
@token_required
def export_consulting_projects(current_user):
    """Export consulting projects to Excel"""
    # Get filters from query parameters
    country = request.args.get('country')
    status = request.args.get('status')
    year = request.args.get('year', type=int)
    client = request.args.get('client')
    search = request.args.get('search')

    # Build query
    query = ConsultingProject.query

    if country:
        query = query.filter(ConsultingProject.country == country)
    if status:
        query = query.filter(ConsultingProject.status == status)
    if year:
        query = query.filter(ConsultingProject.contract_year == year)
    if client:
        query = query.filter(ConsultingProject.client.ilike(f'%{client}%'))
    if search:
        query = query.filter(
            db.or_(
                ConsultingProject.title_kr.ilike(f'%{search}%'),
                ConsultingProject.title_en.ilike(f'%{search}%'),
                ConsultingProject.country.ilike(f'%{search}%'),
                ConsultingProject.client.ilike(f'%{search}%')
            )
        )

    # Order by contract year and number
    query = query.order_by(
        ConsultingProject.contract_year.asc(),
        ConsultingProject.number.asc()
    )

    projects = query.all()

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "해외기술컨설팅"

    # Define headers
    headers = [
        '번호', '수주년도', '진행여부', '국가별', 'X', 'Y',
        '영문사업명', '국문사업명', '사업형태',
        '착수일', '준공일', '용역비(공사)(백만원)', '발주처'
    ]

    # Style for headers
    header_fill = PatternFill(start_color="0A3D62", end_color="0A3D62", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_alignment = Alignment(horizontal="center", vertical="center")

    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment

    # Write data
    for row_num, project in enumerate(projects, 2):
        ws.cell(row=row_num, column=1, value=project.number)
        ws.cell(row=row_num, column=2, value=project.contract_year)
        ws.cell(row=row_num, column=3, value=project.status)
        ws.cell(row=row_num, column=4, value=project.country)
        ws.cell(row=row_num, column=5, value=float(project.longitude) if project.longitude else None)
        ws.cell(row=row_num, column=6, value=float(project.latitude) if project.latitude else None)
        ws.cell(row=row_num, column=7, value=project.title_en)
        ws.cell(row=row_num, column=8, value=project.title_kr)
        ws.cell(row=row_num, column=9, value=project.project_type)
        ws.cell(row=row_num, column=10, value=project.start_date)
        ws.cell(row=row_num, column=11, value=project.end_date)
        ws.cell(row=row_num, column=12, value=float(project.budget) if project.budget else None)
        ws.cell(row=row_num, column=13, value=project.client)

    # Adjust column widths
    column_widths = [8, 10, 10, 15, 12, 12, 35, 35, 20, 12, 12, 15, 20]
    for col_num, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col_num).column_letter].width = width

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='export',
        entity_type='consulting_project',
        description=f'{current_user.name}님이 해외기술용역 프로젝트 {len(projects)}건을 Excel로 다운로드했습니다.',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    # Generate filename with timestamp
    filename = f"해외기술용역_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@consulting_bp.route('/stats', methods=['GET'])
@token_required
def get_consulting_stats(current_user):
    """Get consulting projects statistics"""
    # Total projects
    total = ConsultingProject.query.count()

    # By status
    status_stats = db.session.query(
        ConsultingProject.status,
        db.func.count(ConsultingProject.id)
    ).group_by(ConsultingProject.status).all()

    # By country (top 10)
    country_stats = db.session.query(
        ConsultingProject.country,
        db.func.count(ConsultingProject.id)
    ).group_by(ConsultingProject.country).order_by(
        db.func.count(ConsultingProject.id).desc()
    ).limit(10).all()

    # By year (last 10 years)
    year_stats = db.session.query(
        ConsultingProject.contract_year,
        db.func.count(ConsultingProject.id),
        db.func.sum(ConsultingProject.budget)
    ).group_by(ConsultingProject.contract_year).order_by(
        ConsultingProject.contract_year.desc()
    ).limit(10).all()

    # Total budget
    total_budget = db.session.query(
        db.func.sum(ConsultingProject.budget)
    ).scalar() or 0

    # Projects with coordinates
    with_coords = ConsultingProject.query.filter(
        ConsultingProject.latitude.isnot(None),
        ConsultingProject.longitude.isnot(None)
    ).count()

    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'byStatus': {status: count for status, count in status_stats},
            'byCountry': [{'country': country, 'count': count} for country, count in country_stats],
            'byYear': [
                {
                    'year': year,
                    'count': count,
                    'budget': float(budget) if budget else 0
                }
                for year, count, budget in year_stats
            ],
            'totalBudget': float(total_budget),
            'withCoordinates': with_coords,
            'coordinateRate': round(with_coords / total * 100, 1) if total > 0 else 0
        }
    })


@consulting_bp.route('/countries', methods=['GET'])
@token_required
def get_consulting_countries(current_user):
    """Get list of countries with projects"""
    countries = db.session.query(
        ConsultingProject.country,
        db.func.count(ConsultingProject.id).label('count')
    ).group_by(ConsultingProject.country).order_by(
        ConsultingProject.country.asc()
    ).all()

    return jsonify({
        'success': True,
        'data': [
            {'country': country, 'count': count}
            for country, count in countries
        ]
    })


@consulting_bp.route('/clients', methods=['GET'])
@token_required
def get_consulting_clients(current_user):
    """Get list of clients"""
    clients = db.session.query(
        ConsultingProject.client
    ).filter(
        ConsultingProject.client.isnot(None)
    ).distinct().order_by(
        ConsultingProject.client.asc()
    ).all()

    return jsonify({
        'success': True,
        'data': [client[0] for client in clients if client[0]]
    })
