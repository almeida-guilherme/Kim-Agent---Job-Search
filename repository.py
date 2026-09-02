from database import SessionLocal, Job, VectorDB
from schemas.schemas import JobListing
from utils import get_embedding, extract_cv_text
from langchain_community.utils.math import cosine_similarity
import numpy as np

def save_jobs(jobs: list[JobListing], cv_embedding: list[float]) -> int:
    session = SessionLocal()
    inserted = 0
    try:
        for job in jobs:
            exist = session.query(Job).filter_by(job_posting_id=job.id).first()
            status: str = ""
            if exist:
                continue

            summary = job.summary
            if summary is None:
                summary= "empty"
            current_embedding = get_embedding(summary)

            similarity = cosine_similarity([cv_embedding], [current_embedding])[0][0]

            if similarity > 0.7:
                status = "not applied"
            else:
                status = "job overqualified"

            db_job = Job(
                job_posting_id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                summary=job.summary,
                seniority=job.seniority,
                employment_type=job.employment_type,
                posted_date=job.posted_date,
                url=job.url,
                status = status,
                embedding = current_embedding,
                score = float(similarity)
            )
            session.add(db_job)
            inserted += 1

        session.commit()
        return inserted
    finally:
        session.close()


def save_cv_embedding(document_name:str):
    session = SessionLocal()
    try:
        existing = session.query(VectorDB).filter_by(document_name=document_name).first()
        if existing:
            return existing.embedding

        document_content = extract_cv_text(f"./curriculo/{document_name}")
        embedding = get_embedding(document_content)
        cv_record = VectorDB(document_name=document_name, embedding=embedding)
        session.add(cv_record)
        session.commit()
        return embedding
    finally:
        session.close()