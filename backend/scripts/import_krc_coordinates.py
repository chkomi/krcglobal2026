"""
KRC JSON 파일에서 좌표 정보를 가져와서 프로젝트 데이터베이스에 추가하는 스크립트
"""
import os
import sys
import json
from pathlib import Path

# 프로젝트 루트 디렉토리 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, Project

# 국가명 매핑 (KRC JSON의 국가명과 DB의 국가명이 다를 수 있음)
COUNTRY_MAPPING = {
    "베트남": "베트남",
    "라오스": "라오스",
    "캄보디아": "캄보디아",
    "필리핀": "필리핀",
    "몽골": "몽골",
    "우즈베키스탄": "우즈베키스탄",
    # 필요시 추가 매핑
}


def import_coordinates_from_krc():
    """KRC JSON 파일에서 좌표를 가져와 프로젝트에 추가"""
    
    with app.app_context():
        # KRC 디렉토리 경로
        krc_dir = Path(__file__).parent.parent.parent / 'KRC' / 'data'
        
        if not krc_dir.exists():
            print(f"❌ KRC 데이터 디렉토리를 찾을 수 없습니다: {krc_dir}")
            return
        
        # ODA 데이터 로드
        oda_file = krc_dir / 'global_oda.json'
        consulting_file = krc_dir / 'global_consulting.json'
        
        updated_count = 0
        created_count = 0
        
        # ODA 프로젝트 처리
        if oda_file.exists():
            print(f"📂 ODA 데이터 로드: {oda_file}")
            with open(oda_file, 'r', encoding='utf-8') as f:
                oda_data = json.load(f)
            
            for item in oda_data:
                country = item.get('name', '').strip()
                lat = item.get('lat')
                lng = item.get('lng')
                description = item.get('description', '').strip()
                
                if not country or not lat or not lng:
                    continue
                
                # 프로젝트 찾기 (국가명과 사업명으로 매칭)
                project = Project.query.filter(
                    Project.country == country
                ).filter(
                    db.or_(
                        Project.title.ilike(f'%{description[:20]}%'),
                        Project.description.ilike(f'%{description[:20]}%')
                    )
                ).first()
                
                if project:
                    # 기존 프로젝트에 좌표 추가
                    if not project.latitude or not project.longitude:
                        project.latitude = float(lat)
                        project.longitude = float(lng)
                        updated_count += 1
                        print(f"  ✓ 업데이트: {project.title} ({country})")
                else:
                    # 프로젝트가 없으면 생성 (선택사항)
                    # 주석 처리: 필요시 활성화
                    # project = Project(
                    #     code=f"ODA-{item.get('number', 'UNK')}",
                    #     title=description,
                    #     country=country,
                    #     latitude=float(lat),
                    #     longitude=float(lng),
                    #     project_type='oda_bilateral',
                    #     department='aidc',
                    #     budget_total=item.get('budget', 0) * 1000000,
                    #     status='in_progress'
                    # )
                    # db.session.add(project)
                    # created_count += 1
                    print(f"  ⚠ 찾을 수 없음: {description} ({country})")
        
        # Consulting 프로젝트 처리
        if consulting_file.exists():
            print(f"\n📂 Consulting 데이터 로드: {consulting_file}")
            with open(consulting_file, 'r', encoding='utf-8') as f:
                consulting_data = json.load(f)
            
            for item in consulting_data:
                country = item.get('name', '').strip()
                lat = item.get('lat')
                lng = item.get('lng')
                description = item.get('description', '').strip()
                
                if not country or not lat or not lng:
                    continue
                
                # 프로젝트 찾기
                project = Project.query.filter(
                    Project.country == country
                ).filter(
                    db.or_(
                        Project.title.ilike(f'%{description[:20]}%'),
                        Project.description.ilike(f'%{description[:20]}%')
                    )
                ).first()
                
                if project:
                    if not project.latitude or not project.longitude:
                        project.latitude = float(lat)
                        project.longitude = float(lng)
                        updated_count += 1
                        print(f"  ✓ 업데이트: {project.title} ({country})")
                else:
                    print(f"  ⚠ 찾을 수 없음: {description} ({country})")
        
        # 변경사항 저장
        if updated_count > 0:
            db.session.commit()
            print(f"\n✅ {updated_count}개의 프로젝트에 좌표를 추가했습니다.")
        else:
            print("\nℹ 업데이트할 프로젝트가 없습니다.")
        
        # 좌표가 있는 프로젝트 수 확인
        projects_with_coords = Project.query.filter(
            Project.latitude.isnot(None),
            Project.longitude.isnot(None),
            Project.latitude != 0,
            Project.longitude != 0
        ).count()
        
        print(f"\n📊 현재 좌표가 있는 프로젝트 수: {projects_with_coords}")


if __name__ == '__main__':
    print("=" * 60)
    print("KRC 좌표 정보 가져오기")
    print("=" * 60)
    import_coordinates_from_krc()
    print("=" * 60)

