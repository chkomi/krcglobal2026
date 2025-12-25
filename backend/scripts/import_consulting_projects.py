"""
GBMS - Import Consulting Projects from Excel
해외기술용역 프로젝트 데이터를 Excel에서 가져오기

Run with: python scripts/import_consulting_projects.py
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app import app
from models import db, ConsultingProject


def import_consulting_projects():
    """Import consulting projects from Excel file"""

    # Excel 파일 경로
    excel_file = Path(__file__).parent.parent.parent / 'KRC' / 'data' / 'global consulting.xlsx'

    if not excel_file.exists():
        print(f"❌ Excel 파일을 찾을 수 없습니다: {excel_file}")
        return

    print(f"📂 Excel 파일 로드: {excel_file}")

    with app.app_context():
        # Excel 파일 읽기
        df = pd.read_excel(excel_file, sheet_name="해외기술컨설팅('72-'25)")

        print(f"📊 총 {len(df)}개의 프로젝트 데이터를 찾았습니다.")

        # 기존 데이터 확인
        existing_count = ConsultingProject.query.count()
        if existing_count > 0:
            print(f"⚠️  기존 데이터 {existing_count}개가 있습니다.")
            response = input("기존 데이터를 삭제하고 다시 임포트하시겠습니까? (y/N): ")
            if response.lower() == 'y':
                ConsultingProject.query.delete()
                db.session.commit()
                print("✓ 기존 데이터를 삭제했습니다.")
            else:
                print("❌ 임포트를 취소했습니다.")
                return

        # 데이터 임포트
        imported_count = 0
        skipped_count = 0

        for idx, row in df.iterrows():
            try:
                # 필수 필드 검증
                if pd.isna(row['국문사업명']) or pd.isna(row['국가별']):
                    print(f"  ⚠ 행 {idx + 2}: 필수 필드 누락 - 건너뜀")
                    skipped_count += 1
                    continue

                # ConsultingProject 생성
                project = ConsultingProject(
                    number=int(row['번호']) if pd.notna(row['번호']) else None,
                    contract_year=int(row['수주년도']) if pd.notna(row['수주년도']) else None,
                    status=row['진행여부'] if pd.notna(row['진행여부']) else '준공',
                    country=row['국가별'].strip(),
                    longitude=float(row['X']) if pd.notna(row['X']) else None,
                    latitude=float(row['Y']) if pd.notna(row['Y']) else None,
                    title_en=row['영문사업명'] if pd.notna(row['영문사업명']) else None,
                    title_kr=row['국문사업명'].strip(),
                    project_type=row['사업형태'] if pd.notna(row['사업형태']) else None,
                    start_date=str(row['착수일']) if pd.notna(row['착수일']) else None,
                    end_date=str(row['준공일']) if pd.notna(row['준공일']) else None,
                    budget=float(row['용역비(공사)(백만원)']) if pd.notna(row['용역비(공사)(백만원)']) else None,
                    client=row['발주처'] if pd.notna(row['발주처']) else None
                )

                db.session.add(project)
                imported_count += 1

                # 진행상황 표시 (10개마다)
                if imported_count % 10 == 0:
                    print(f"  ⏳ {imported_count}개 처리 중...")

            except Exception as e:
                print(f"  ❌ 행 {idx + 2} 처리 중 오류: {e}")
                skipped_count += 1
                continue

        # 데이터베이스에 저장
        try:
            db.session.commit()
            print(f"\n✅ 임포트 완료!")
            print(f"  - 성공: {imported_count}개")
            print(f"  - 건너뜀: {skipped_count}개")
            print(f"  - 총: {imported_count + skipped_count}개")

            # 통계 출력
            print("\n📊 임포트 통계:")

            # 국가별 통계
            country_stats = db.session.query(
                ConsultingProject.country,
                db.func.count(ConsultingProject.id)
            ).group_by(ConsultingProject.country).order_by(
                db.func.count(ConsultingProject.id).desc()
            ).limit(10).all()

            print("\n  국가별 프로젝트 수 (상위 10개):")
            for country, count in country_stats:
                print(f"    - {country}: {count}개")

            # 상태별 통계
            status_stats = db.session.query(
                ConsultingProject.status,
                db.func.count(ConsultingProject.id)
            ).group_by(ConsultingProject.status).all()

            print("\n  상태별 프로젝트 수:")
            for status, count in status_stats:
                print(f"    - {status}: {count}개")

            # 좌표가 있는 프로젝트 수
            coords_count = ConsultingProject.query.filter(
                ConsultingProject.latitude.isnot(None),
                ConsultingProject.longitude.isnot(None)
            ).count()

            print(f"\n  좌표가 있는 프로젝트: {coords_count}개 ({coords_count/imported_count*100:.1f}%)")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 데이터베이스 저장 중 오류 발생: {e}")


if __name__ == '__main__':
    print("=" * 70)
    print("해외기술용역 프로젝트 임포트")
    print("=" * 70)
    import_consulting_projects()
    print("=" * 70)
