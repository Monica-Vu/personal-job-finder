"""
Company configurations for Workday job boards
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from constants import JobPostingAgeKey

@dataclass
@dataclass
class CompanyConfig:
    """Configuration for a single company's job API."""
    api_url: str
    http_method: str = "POST"
    body: Optional[Dict[str, Any]] = None
    parser_key: str = "workday"
    job_id_key: str = "bulletFields"
    job_age_key: str = "postedOn"    
    
# Company configurations - add new companies here
COMPANY_CONFIGS = {
    # "clio": CompanyConfig(
    #     api_url="https://clio.wd3.myworkdayjobs.com/wday/cxs/clio/ClioCareerSite/jobs",
    #     body={
    #     "appliedFacets": {
    #         "locations": [
    #             "1b6969fbfbca0101f164999ecea20000",
    #             "951c033a9bfe1000baf025938f160000",
    #             "29827a73287b01033875f6106f2c0000"
    #         ],
    #         "jobFamilyGroup": [
    #             "29827a73287b0103383979088de50000"
    #         ]
    #     },
    #     "limit": 20,
    #     "offset": 0,
    #     "searchText": "Software+Developer"
    #     },
    #     job_age_key=JobPostingAgeKey.POSTED_ON
    # ),
    # "crowdstrike": CompanyConfig(
    #     api_url = "https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs",
    #     body = {
    #         "appliedFacets":{
    #             "locationCountry":[
    #                 "a30a87ed25634629aa6c3958aa2b91ea"
    #             ],
    #             "Job_Family":[
    #                 "1408861ee6e201641be2c2f6b000c00b"
    #             ],
    #             "locations":[
    #                 "27086a67c269015eef3a02793f019508"
    #             ]
    #         },
    #         "limit":20,
    #         "offset":0,
    #         "searchText":""
    #         },
    #      job_age_key=JobPostingAgeKey.POSTED_ON
    # ),
    # "remitly": CompanyConfig(
    #     api_url = "https://remitly.wd5.myworkdayjobs.com/wday/cxs/remitly/Remitly_Careers/jobs",
    #     body = {
    #     "appliedFacets": {
    #         "locationCountry": [
    #             "a30a87ed25634629aa6c3958aa2b91ea"
    #         ],
    #         "jobFamilyGroup": [
    #             "c9699b32e2da1029a051260e906d0000"
    #         ]
    #     },
    #     "limit": 20,
    #     "offset": 0,
    #     "searchText": "Software+Developer"
    #     },
    #     job_age_key=JobPostingAgeKey.POSTED_ON
    # ),
    # "openlane": CompanyConfig(
    #     api_url = "https://kar.wd1.myworkdayjobs.com/wday/cxs/kar/OPENLANE_Careers/jobs",
    #     body = {
    #     "appliedFacets": {
    #     "jobFamilyGroup": [
    #         "1feabb51d74b0122d6b8a81cb700682d"
    #     ],
    #     "Location_Region_State_Province": [
    #         "cb76ca97a13347548a188f23caa96b17"
    #     ],
    #     "Location_Country": [
    #         "a30a87ed25634629aa6c3958aa2b91ea"
    #     ]
    #         },
    #         "limit": 20,
    #         "offset": 0,
    #         "searchText": ""
    #     },
    #     job_age_key=JobPostingAgeKey.POSTED_ON
    # ),
    # "weirmotors": CompanyConfig(
    #     api_url="https://weir.wd3.myworkdayjobs.com/wday/cxs/weir/Weir_External_Careers/jobs",
    #     body={
    #     "appliedFacets": {
    #         "Country": [
    #             "a30a87ed25634629aa6c3958aa2b91ea"
    #         ],
    #         "Region_State_Province": [
    #             "cb76ca97a13347548a188f23caa96b17"
    #         ],
    #         "jobFamilyGroup": [
    #             "c8ebc28620ef01501164ed0d01011278"
    #         ]
    #     },
    #     "limit": 20,
    #     "offset": 0,
    #     "searchText": "Software+Developer"
    #     }
    # ),
    "unbounce": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/unbounce/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key= "first_published",
    ),
    "take-two": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/taketwo/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="requisition_id",
        job_age_key= "first_published",
    ),
    "samsara": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/samsara/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="requisition_id",
        job_age_key= "first_published"
    )
}

"""
 TODO: 
 - go through entire script
 - create a script to filter out jobs for greenhouse (location, title, requestion_id - ?)

 """