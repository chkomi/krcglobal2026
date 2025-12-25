"""
GBMS - Database Models
글로벌사업처 해외사업관리시스템
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """사용자 모델"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    department = db.Column(db.String(50), nullable=False)  # gad, gb, aidc
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        dept_names = {
            'gad': '글로벌농업개발부',
            'gb': '글로벌사업부',
            'aidc': '농식품국제개발협력센터'
        }
        return {
            'id': self.id,
            'userId': self.user_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'departmentName': dept_names.get(self.department, self.department),
            'role': self.role,
            'phone': self.phone,
            'position': self.position,
            'isActive': self.is_active
        }


class Project(db.Model):
    """사업 모델"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    project_type = db.Column(db.String(50), nullable=False, index=True)
    # Types: consulting, oda_bilateral, oda_multilateral, k_rice_belt, investment, loan_support
    
    country = db.Column(db.String(50), nullable=False, index=True)
    country_code = db.Column(db.String(3))
    region = db.Column(db.String(50))
    
    # GIS coordinates
    latitude = db.Column(db.Numeric(10, 7))  # 위도
    longitude = db.Column(db.Numeric(10, 7))  # 경도
    
    department = db.Column(db.String(50), nullable=False, index=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    description = db.Column(db.Text)
    objectives = db.Column(db.Text)
    scope = db.Column(db.Text)
    
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration_months = db.Column(db.Integer)
    
    budget_total = db.Column(db.Numeric(15, 2), default=0)
    budget_krw = db.Column(db.Numeric(15, 2), default=0)  # 원화 예산
    budget_foreign = db.Column(db.Numeric(15, 2), default=0)  # 외화 예산
    currency = db.Column(db.String(10), default='KRW')
    
    status = db.Column(db.String(20), default='planning', index=True)
    # Status: planning, bidding, contracted, in_progress, completed, suspended, cancelled
    progress = db.Column(db.Integer, default=0)  # 0-100
    
    client = db.Column(db.String(200))  # 발주처
    partner = db.Column(db.String(200))  # 협력기관
    funding_source = db.Column(db.String(100))  # 재원조달처
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    manager = db.relationship('User', foreign_keys=[manager_id])
    phases = db.relationship('ProjectPhase', backref='project', lazy='dynamic')
    budgets = db.relationship('Budget', backref='project', lazy='dynamic')
    documents = db.relationship('Document', backref='project', lazy='dynamic')
    personnel = db.relationship('ProjectPersonnel', backref='project', lazy='dynamic')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'titleEn': self.title_en,
            'projectType': self.project_type,
            'country': self.country,
            'countryCode': self.country_code,
            'region': self.region,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'department': self.department,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'budgetTotal': float(self.budget_total) if self.budget_total else 0,
            'status': self.status,
            'progress': self.progress,
            'client': self.client
        }
        
        if include_details:
            data.update({
                'description': self.description,
                'objectives': self.objectives,
                'scope': self.scope,
                'durationMonths': self.duration_months,
                'budgetKrw': float(self.budget_krw) if self.budget_krw else 0,
                'budgetForeign': float(self.budget_foreign) if self.budget_foreign else 0,
                'currency': self.currency,
                'partner': self.partner,
                'fundingSource': self.funding_source,
                'manager': self.manager.to_dict() if self.manager else None,
                'createdAt': self.created_at.isoformat() if self.created_at else None,
                'updatedAt': self.updated_at.isoformat() if self.updated_at else None
            })
        
        return data


class ProjectPhase(db.Model):
    """사업단계 모델"""
    __tablename__ = 'project_phases'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    progress = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'projectId': self.project_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'progress': self.progress
        }


class Budget(db.Model):
    """예산 모델"""
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False)
    # Categories: personnel, equipment, travel, operating, subcontract, indirect, other
    
    sub_category = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    amount_planned = db.Column(db.Numeric(15, 2), default=0)
    amount_executed = db.Column(db.Numeric(15, 2), default=0)
    amount_remaining = db.Column(db.Numeric(15, 2), default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    executions = db.relationship('BudgetExecution', backref='budget', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'projectId': self.project_id,
            'year': self.year,
            'category': self.category,
            'subCategory': self.sub_category,
            'description': self.description,
            'amountPlanned': float(self.amount_planned) if self.amount_planned else 0,
            'amountExecuted': float(self.amount_executed) if self.amount_executed else 0,
            'amountRemaining': float(self.amount_remaining) if self.amount_remaining else 0,
            'executionRate': round(float(self.amount_executed) / float(self.amount_planned) * 100, 1) if self.amount_planned else 0
        }


class BudgetExecution(db.Model):
    """예산집행 모델"""
    __tablename__ = 'budget_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False, index=True)
    execution_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    description = db.Column(db.Text)
    voucher_no = db.Column(db.String(50))  # 전표번호
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'budgetId': self.budget_id,
            'executionDate': self.execution_date.isoformat() if self.execution_date else None,
            'amount': float(self.amount) if self.amount else 0,
            'description': self.description,
            'voucherNo': self.voucher_no
        }


class Document(db.Model):
    """문서 모델"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), index=True)
    
    title = db.Column(db.String(200), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)
    # Types: proposal, contract, report, meeting, correspondence, other
    
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(20))
    
    description = db.Column(db.Text)
    version = db.Column(db.String(20), default='1.0')
    
    is_public = db.Column(db.Boolean, default=False)
    department = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'projectId': self.project_id,
            'title': self.title,
            'docType': self.doc_type,
            'fileName': self.file_name,
            'fileSize': self.file_size,
            'fileType': self.file_type,
            'description': self.description,
            'version': self.version,
            'isPublic': self.is_public,
            'department': self.department,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'createdBy': self.creator.name if self.creator else None
        }


class Office(db.Model):
    """해외사무소 모델"""
    __tablename__ = 'offices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(3))
    region = db.Column(db.String(50))
    city = db.Column(db.String(50))
    address = db.Column(db.String(300))
    
    office_type = db.Column(db.String(50))  # regular, oda_desk
    status = db.Column(db.String(20), default='active')
    
    contact_person = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(50))
    
    established_date = db.Column(db.Date)
    annual_budget = db.Column(db.Numeric(15, 2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'countryCode': self.country_code,
            'region': self.region,
            'city': self.city,
            'address': self.address,
            'officeType': self.office_type,
            'status': self.status,
            'contactPerson': self.contact_person,
            'contactEmail': self.contact_email,
            'contactPhone': self.contact_phone,
            'establishedDate': self.established_date.isoformat() if self.established_date else None,
            'annualBudget': float(self.annual_budget) if self.annual_budget else 0
        }


class ProjectPersonnel(db.Model):
    """사업인력 모델"""
    __tablename__ = 'project_personnel'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))  # PM, 팀장, 팀원, 전문가 등
    position = db.Column(db.String(100))
    affiliation = db.Column(db.String(200))  # 소속
    
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_deployed = db.Column(db.Boolean, default=False)  # 파견 여부
    
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'projectId': self.project_id,
            'name': self.name,
            'role': self.role,
            'position': self.position,
            'affiliation': self.affiliation,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'isDeployed': self.is_deployed,
            'contactEmail': self.contact_email,
            'contactPhone': self.contact_phone
        }


class ActivityLog(db.Model):
    """활동 로그 모델"""
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, login, logout
    entity_type = db.Column(db.String(50))  # project, document, budget, etc.
    entity_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', foreign_keys=[user_id])

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userName': self.user.name if self.user else None,
            'action': self.action,
            'entityType': self.entity_type,
            'entityId': self.entity_id,
            'description': self.description,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class ConsultingProject(db.Model):
    """해외기술용역 프로젝트 모델"""
    __tablename__ = 'consulting_projects'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True)  # 번호
    contract_year = db.Column(db.Integer, index=True)  # 수주년도
    status = db.Column(db.String(20), default='준공', index=True)  # 진행여부: 준공, 진행중

    country = db.Column(db.String(100), nullable=False, index=True)  # 국가별
    latitude = db.Column(db.Numeric(10, 7))  # Y (위도)
    longitude = db.Column(db.Numeric(10, 7))  # X (경도)

    title_en = db.Column(db.String(500))  # 영문사업명
    title_kr = db.Column(db.String(500), nullable=False)  # 국문사업명
    project_type = db.Column(db.String(200))  # 사업형태

    start_date = db.Column(db.String(20))  # 착수일 (예: '72-10)
    end_date = db.Column(db.String(20))  # 준공일 (예: '73-09)

    budget = db.Column(db.Numeric(15, 2))  # 용역비(공사)(백만원)
    client = db.Column(db.String(200))  # 발주처

    # 메타 정보
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'contractYear': self.contract_year,
            'status': self.status,
            'country': self.country,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'titleEn': self.title_en,
            'titleKr': self.title_kr,
            'projectType': self.project_type,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'budget': float(self.budget) if self.budget else 0,
            'client': self.client,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'createdBy': self.creator.name if self.creator else None
        }
