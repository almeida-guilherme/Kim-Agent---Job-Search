from pydantic import BaseModel, Field
from typing import Optional

class JobListing(BaseModel):
    title: Optional[str] = Field(default=None, alias="job_title")
    id: Optional[str] = Field(default=None, alias="job_posting_id")
    company: Optional[str] = Field(default=None, alias="company_name")
    location: Optional[str] = Field(default=None, alias="job_location")
    summary: Optional[str] = Field(default=None, alias="job_summary")
    seniority: Optional[str] = Field(default=None, alias="job_seniority_level")
    employment_type: Optional[str] = Field(default=None, alias="job_employment_type")
    posted_date: Optional[str] = Field(default=None, alias="job_posted_date")
    url: Optional[str] = None
    applicants: Optional[int] = Field(default=None, alias="job_num_applicants")

    class Config:
        populate_by_name = True  