from sqlalchemy import create_engine, Column, String, Integer, text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    job_posting_id = Column(String, primary_key = True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    summary = Column(String)
    seniority = Column(String)
    employment_type = Column(String)
    url = Column(String)
    status = Column(String)
    embedding = Column(Vector(1536), nullable=True)
    posted_date=Column(String)
    score = Column(Integer)

class VectorDB(Base):
    __tablename__ = "cv-embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String)
    embedding = Column(Vector(1536)) 

def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(engine)