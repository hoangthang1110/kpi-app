from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/kpi")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String)
    uploader = Column(String)
    upload_time = Column(TIMESTAMP, default=datetime.utcnow)
    word_count = Column(Integer)
    kpi_score = Column(Integer)
    missing_5w1h = Column(Integer)
    sentence_count = Column(Integer)
    pos_counts_json = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
