import httpx
import asyncio
from dotenv import load_dotenv
import os
from schemas.schemas import JobListing

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATASET_ID = os.getenv("DATASET_ID")

#this function is important to structure the output of the API return. That's why it was used the Pydantic model
def parse_jobs(raw_data: list[dict]) -> list[JobListing]:
    job_list: list[JobListing] = [JobListing(**job) for job in raw_data]
    job_list_filtered: list[JobListing]  = job_filter(job_list)
    return job_list_filtered

#API call
async def trigger_linkedin_search(keyword: str, location: str = "Brazil", remote: str = "") -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.brightdata.com/datasets/v3/trigger",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={
                "dataset_id": DATASET_ID,
                "type": "discover_new",
                "discover_by": "keyword",
                "limit_per_input": 5
            },

            json=[{
                "keyword": keyword,
                "location": location,
                "country": "",
                "time_range": "",
                "job_type": "",
                "experience_level": "",
                "remote": remote,
                "company": "",
                "location_radius": ""
            }]
        )
        data = resp.json()
        snapshot_id = data.get("snapshot_id")
        if not snapshot_id:
            raise Exception(f"Erro ao disparar trigger: {data}")
        return snapshot_id

#After the API call, it is necessary to wait the return. This is function is about it
async def poll_snapshot(snapshot_id: str, interval: int = 30, timeout: int = 600) -> list[JobListing]:
    elapsed = 0
    async with httpx.AsyncClient() as client:
        while elapsed < timeout:
            result = await client.get(
                f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                params={"format": "json"}
            )
            data = result.json()

            if isinstance(data, dict) and data.get("status") == "running":
                print(f"Ainda rodando, aguardando {interval}s...")
                await asyncio.sleep(interval)
                elapsed += interval
                continue

            if isinstance(data, list):
                return parse_jobs(data)

            raise Exception(f"Resposta inesperada do snapshot: {data}")

        raise TimeoutError("Snapshot demorou demais para ficar pronto.")

#Job filter
def job_filter(jobs:list[JobListing]) -> list[JobListing]:
    excluded_terms = ["ML","Machine Learning"]

    return [
        job for job in jobs
        if not any(term in (job.title or "") for term in excluded_terms)
    ]

#Call all the functions to get the LinkedIn jobs
async def search_linkedin_jobs(keyword: str, location: str = "Brazil") -> list[JobListing]:
    snapshot_id = await trigger_linkedin_search(keyword, location)
    print("Snapshot ID:", snapshot_id)
    return await poll_snapshot(snapshot_id)
