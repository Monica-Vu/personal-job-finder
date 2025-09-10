"""
Company configurations for Workday job boards
"""

from typing import List
from dataclasses import dataclass


@dataclass
class CompanyConfig:
    """Configuration for a company's Workday job board"""
    name: str
    api_url: str
    search_text: str
    location_ids: List[str]
    job_family_group: List[str]
    job_display_limit: int = 20
    # Optional: Custom facet keys for different Workday implementations
    location_facet_key: str = "locations"  # Default: "locations", CrowdStrike uses "locationCountry", OpenLane uses "primaryLocation"
    job_family_facet_key: str = "jobFamilyGroup"  # Default: "jobFamilyGroup", CrowdStrike uses "Job_Family"
    # For companies that need multiple location facet types (like Remitly)
    location_country_ids: List[str] = None  # Optional: for locationCountry facet
    location_country_facet_key: str = "locationCountry"  # Default: "locationCountry"


# Company configurations - add new companies here
COMPANY_CONFIGS = {
    "clio": CompanyConfig(
        name="Clio",
        api_url="https://clio.wd3.myworkdayjobs.com/wday/cxs/clio/ClioCareerSite/jobs",
        search_text="Software Developer",
        location_ids=[
            "1b6969fbfbca0101f164999ecea20000",  # Vancouver, BC
            "951c033a9bfe1000baf025938f160000"   # Remote, Canada
        ],
        job_family_group=["29827a73287b0103383979088de50000"],
    ),
    "crowdstrike": CompanyConfig(
        name="CrowdStrike",
        api_url="https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs",
        search_text="",
        location_ids=["a30a87ed25634629aa6c3958aa2b91ea"],  # Example location ID
        job_family_group=["1408861ee6e201641be2c2f6b000c00b"],  # Example job family ID
        location_facet_key="locationCountry",  # CrowdStrike uses "locationCountry"
        job_family_facet_key="Job_Family"  # CrowdStrike uses "Job_Family"
    ),
    "remitly": CompanyConfig(
        name="Remitly",
        api_url="https://remitly.wd5.myworkdayjobs.com/wday/cxs/remitly/Remitly_Careers/jobs",
        search_text="",  # Empty search text to get all jobs
        location_ids=["2458716c04a71002062e0e03eb960000"],  # New Westminster, British Columbia, Canada
        job_family_group=["c9699b32e2da1029a051260e906d0000"],  # Software Engineering job family
        location_facet_key="locations",  # Standard Workday facet key
        job_family_facet_key="jobFamilyGroup",  # Standard Workday facet key
        location_country_ids=["a30a87ed25634629aa6c3958aa2b91ea"],  # Canada (from locationCountry)
        location_country_facet_key="locationCountry"  # Standard Workday facet key
    ),
    "openlane": CompanyConfig(
        name="OpenLane",
        api_url="https://kar.wd1.myworkdayjobs.com/wday/cxs/kar/OPENLANE_Careers/jobs",
        search_text="",  # Empty search text to get all jobs
        location_ids=["f1945455dade1001a7c8e263fef60000"],  # Primary location from curl
        job_family_group=["1feabb51d74b0122d6b8a81cb700682d"],  # Job family group from curl
        location_facet_key="primaryLocation",  # OpenLane uses "primaryLocation" instead of "locations"
        job_family_facet_key="jobFamilyGroup"  # Standard Workday facet key
    ),
    # Add more companies here as needed
    # Example:
    # "company_name": CompanyConfig(
    #     name="Company Name",
    #     api_url="https://company.wd3.myworkdayjobs.com/wday/cxs/company/CareerSite/jobs",
    #     search_text="Software Developer",
    #     location_ids=["location_id_1", "location_id_2"],
    #     job_family_group=["job_family_id"],
    #     job_display_limit=20
    # ),
}
