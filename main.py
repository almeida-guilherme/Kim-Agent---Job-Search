from searchJobs import search_linkedin_jobs
from database import init_db
from repository import save_jobs, save_cv_embedding
import asyncio

async def main():
    init_db()
    jobs = await search_linkedin_jobs("Artificial Engineer")
    if len(jobs)>0:
        cv = save_cv_embedding("CV - Guilherme Almeida.pdf")
        saved_jobs = save_jobs(jobs,cv)

    if saved_jobs == 0:
        print("0 inseridos")
    else:
        print(f"inserido {saved_jobs}")

    for job in jobs:
        print(f"- {job.title} @ {job.company} ({job.location})")
        print(f"  {job.url}\n")
        print(f"  {job.id}\n")


if __name__ == "__main__":
    asyncio.run(main())

