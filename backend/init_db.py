"""
GBMS - Database Initialization Script
글로벌사업처 해외사업관리시스템 - 초기 데이터 생성

Run with: python init_db.py
"""
import os
import sys
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Project, Budget, Office


def init_database():
    """Initialize database with tables and sample data"""
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Enable WAL mode for SQLite
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            db.engine.execute('PRAGMA journal_mode=WAL')
            db.engine.execute('PRAGMA synchronous=NORMAL')
            db.engine.execute('PRAGMA cache_size=-64000')
        
        print("✓ 데이터베이스 테이블 생성 완료")
        
        # Check if admin user exists
        admin = User.query.filter_by(user_id='admin').first()
        if not admin:
            create_sample_data()
            print("✓ 샘플 데이터 생성 완료")
        else:
            print("ℹ 기존 데이터가 존재합니다. 샘플 데이터를 건너뜁니다.")
        
        print("\n🎉 데이터베이스 초기화 완료!")
        print("\n테스트 계정:")
        print("  - admin / admin123 (관리자)")
        print("  - user1 / user123 (글로벌사업부)")
        print("  - user2 / user123 (농식품국제개발협력센터)")


def create_sample_data():
    """Create sample data for testing"""
    
    # Create users
    users = [
        {
            'user_id': 'admin',
            'name': '관리자',
            'email': 'admin@krc.co.kr',
            'department': 'gad',
            'role': 'admin',
            'position': '팀장',
            'password': 'admin123'
        },
        {
            'user_id': 'user1',
            'name': '홍길동',
            'email': 'hong@krc.co.kr',
            'department': 'gb',
            'role': 'user',
            'position': '대리',
            'password': 'user123'
        },
        {
            'user_id': 'user2',
            'name': '김철수',
            'email': 'kim@krc.co.kr',
            'department': 'aidc',
            'role': 'user',
            'position': '주임',
            'password': 'user123'
        }
    ]
    
    created_users = {}
    for u in users:
        user = User(
            user_id=u['user_id'],
            name=u['name'],
            email=u['email'],
            department=u['department'],
            role=u['role'],
            position=u['position']
        )
        user.set_password(u['password'])
        db.session.add(user)
        created_users[u['user_id']] = user
    
    db.session.commit()
    
    # Create sample projects
    projects = [
        {
            'code': 'PRJ-2024-001',
            'title': '캄보디아 관개시설 현대화 사업',
            'title_en': 'Cambodia Irrigation Modernization Project',
            'project_type': 'consulting',
            'country': '캄보디아',
            'country_code': 'KH',
            'region': '아시아',
            'department': 'gb',
            'description': '캄보디아 농업생산성 향상을 위한 관개시설 현대화 기술컨설팅',
            'start_date': date(2023, 3, 1),
            'end_date': date(2025, 2, 28),
            'budget_total': 1500000000,
            'status': 'in_progress',
            'progress': 85,
            'client': 'KOICA'
        },
        {
            'code': 'PRJ-2024-002',
            'title': '베트남 스마트팜 구축 ODA',
            'title_en': 'Vietnam Smart Farm Development ODA',
            'project_type': 'oda_bilateral',
            'country': '베트남',
            'country_code': 'VN',
            'region': '아시아',
            'department': 'aidc',
            'description': '베트남 중부지역 스마트팜 시범단지 구축 지원',
            'start_date': date(2024, 1, 1),
            'end_date': date(2026, 12, 31),
            'budget_total': 5000000000,
            'status': 'in_progress',
            'progress': 45,
            'client': '농림축산식품부'
        },
        {
            'code': 'PRJ-2024-003',
            'title': '필리핀 K-라이스벨트 시범사업',
            'title_en': 'Philippines K-Rice Belt Pilot Project',
            'project_type': 'k_rice_belt',
            'country': '필리핀',
            'country_code': 'PH',
            'region': '아시아',
            'department': 'aidc',
            'description': 'K-라이스벨트 전략의 일환으로 필리핀 루손섬 지역 벼농사 기술지원',
            'start_date': date(2024, 6, 1),
            'end_date': date(2027, 5, 31),
            'budget_total': 8000000000,
            'status': 'planning',
            'progress': 20,
            'client': '농림축산식품부'
        },
        {
            'code': 'PRJ-2024-004',
            'title': '우즈베키스탄 농업용수관리 컨설팅',
            'title_en': 'Uzbekistan Agricultural Water Management Consulting',
            'project_type': 'consulting',
            'country': '우즈베키스탄',
            'country_code': 'UZ',
            'region': '중앙아시아',
            'department': 'gb',
            'description': '우즈베키스탄 농업용수 효율화를 위한 기술컨설팅',
            'start_date': date(2022, 1, 1),
            'end_date': date(2024, 6, 30),
            'budget_total': 2000000000,
            'status': 'completed',
            'progress': 100,
            'client': 'AfDB'
        },
        {
            'code': 'PRJ-2024-005',
            'title': '탄자니아 농촌개발 협력사업',
            'title_en': 'Tanzania Rural Development Cooperation',
            'project_type': 'oda_multilateral',
            'country': '탄자니아',
            'country_code': 'TZ',
            'region': '아프리카',
            'department': 'aidc',
            'description': 'FAO 협력 탄자니아 농촌개발 다자성양자 사업',
            'start_date': date(2024, 4, 1),
            'end_date': date(2028, 3, 31),
            'budget_total': 12000000000,
            'status': 'in_progress',
            'progress': 30,
            'client': 'FAO'
        },
        {
            'code': 'PRJ-2024-006',
            'title': '인도네시아 해외농업개발 타당성조사',
            'title_en': 'Indonesia Agricultural Investment Feasibility Study',
            'project_type': 'investment',
            'country': '인도네시아',
            'country_code': 'ID',
            'region': '아시아',
            'department': 'gb',
            'description': '인도네시아 농업투자개발 대상지 타당성 조사',
            'start_date': date(2024, 9, 1),
            'end_date': date(2025, 2, 28),
            'budget_total': 300000000,
            'status': 'planning',
            'progress': 10,
            'client': '한국농어촌공사'
        }
    ]
    
    created_projects = []
    for p in projects:
        project = Project(**p, created_by=created_users['admin'].id)
        db.session.add(project)
        created_projects.append(project)
    
    db.session.commit()
    
    # 샘플 프로젝트에 좌표 추가 (KRC 스타일)
    # 실제 사용 시 KRC JSON 파일에서 좌표를 가져와야 함
    coordinates = {
        '캄보디아': {'lat': 11.5564, 'lng': 104.9282},
        '베트남': {'lat': 14.0583, 'lng': 108.2772},
        '필리핀': {'lat': 12.8797, 'lng': 121.7740},
        '우즈베키스탄': {'lat': 41.3775, 'lng': 64.5853},
        '탄자니아': {'lat': -6.3690, 'lng': 34.8888},
        '인도네시아': {'lat': -0.7893, 'lng': 113.9213}
    }
    
    for project in created_projects:
        if project.country in coordinates:
            project.latitude = coordinates[project.country]['lat']
            project.longitude = coordinates[project.country]['lng']
    
    db.session.commit()
    
    # Create sample budgets
    current_year = datetime.now().year
    for project in created_projects:
        categories = ['personnel', 'travel', 'equipment', 'operating', 'subcontract']
        for i, cat in enumerate(categories):
            planned = float(project.budget_total) * (0.3 - i * 0.05)
            executed = planned * (project.progress / 100) if project.status != 'planning' else 0
            
            budget = Budget(
                project_id=project.id,
                year=current_year,
                category=cat,
                amount_planned=planned,
                amount_executed=executed,
                amount_remaining=planned - executed
            )
            db.session.add(budget)
    
    db.session.commit()
    
    # Create sample offices
    offices = [
        {
            'name': '캄보디아사무소',
            'country': '캄보디아',
            'country_code': 'KH',
            'region': '아시아',
            'city': '프놈펜',
            'office_type': 'regular',
            'status': 'active',
            'contact_person': '박지원',
            'contact_email': 'cambodia@krc.co.kr',
            'established_date': date(2015, 3, 1),
            'annual_budget': 500000000
        },
        {
            'name': '베트남사무소',
            'country': '베트남',
            'country_code': 'VN',
            'region': '아시아',
            'city': '하노이',
            'office_type': 'regular',
            'status': 'active',
            'contact_person': '이영희',
            'contact_email': 'vietnam@krc.co.kr',
            'established_date': date(2018, 7, 1),
            'annual_budget': 450000000
        },
        {
            'name': '탄자니아 ODA데스크',
            'country': '탄자니아',
            'country_code': 'TZ',
            'region': '아프리카',
            'city': '다르에스살람',
            'office_type': 'oda_desk',
            'status': 'active',
            'contact_person': '김민수',
            'contact_email': 'tanzania@krc.co.kr',
            'established_date': date(2022, 1, 1),
            'annual_budget': 200000000
        },
        {
            'name': '필리핀사무소',
            'country': '필리핀',
            'country_code': 'PH',
            'region': '아시아',
            'city': '마닐라',
            'office_type': 'regular',
            'status': 'active',
            'contact_person': '정수민',
            'contact_email': 'philippines@krc.co.kr',
            'established_date': date(2020, 5, 1),
            'annual_budget': 400000000
        }
    ]
    
    for o in offices:
        office = Office(**o)
        db.session.add(office)
    
    db.session.commit()


if __name__ == '__main__':
    init_database()
