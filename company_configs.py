"""
Company configurations for Workday job boards
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from constants import JobPostingAgeKey

@dataclass
class CompanyConfig:
    api_url: str
    http_method: str = "POST"
    body: Optional[Dict[str, Any]] = None
    job_age_key: JobPostingAgeKey = JobPostingAgeKey.POSTED_ON

# Company configurations - add new companies here
COMPANY_CONFIGS = {
    "clio": CompanyConfig(
        api_url="https://clio.wd3.myworkdayjobs.com/wday/cxs/clio/ClioCareerSite/jobs",
        body={
        "appliedFacets": {
            "locations": [
                "1b6969fbfbca0101f164999ecea20000",
                "951c033a9bfe1000baf025938f160000",
                "29827a73287b01033875f6106f2c0000"
            ],
            "jobFamilyGroup": [
                "29827a73287b0103383979088de50000"
            ]
        },
        "limit": 20,
        "offset": 0,
        "searchText": "Software+Developer"
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "crowdstrike": CompanyConfig(
        api_url = "https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs",
        body = {
            "appliedFacets": {
                "locationCountry": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ],
                "Job_Family": [
                    "1408861ee6e201641be2c2f6b000c00b"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
            },
         job_age_key=JobPostingAgeKey.POSTED_ON
    )
}
