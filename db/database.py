from sqlalchemy import Column, Integer, String, Float, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Date, create_engine
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:password@localhost:5432/kpi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploader = Column(String)
    word_count = Column(Integer)
    kpi_score = Column(Float)
    missing_5w1h = Column(Integer)
    sentence_count = Column(Integer)
    pos_counts_json = Column(JSON)
    complexity = Column(String)
    completed_in_minutes = Column(Integer)
# Bổ sung vào sau class Document

class KPITarget(Base):
    __tablename__ = "kpi_targets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    target_value = Column(Float)
    unit = Column(String)
    deadline = Column(Date)

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("kpi_targets.id"))
    assigned_date = Column(Date)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="assignments")
    target = relationship("KPITarget")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)  # admin, leader, staff

    assignments = relationship("Assignment", back_populates="user")

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
# Thêm sau cùng
# Tạo bảng
Base.metadata.create_all(bind=engine)
