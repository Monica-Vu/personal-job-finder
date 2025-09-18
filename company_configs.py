from typing import Dict, Any, Optional
from dataclasses import dataclass
from constants import JobPostingAgeKey

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
    # WORKDAY
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
        api_url="https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs",
        body={
            "appliedFacets": {
                "locationCountry": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ],
                "Job_Family": [
                    "1408861ee6e201641be2c2f6b000c00b"
                ],
                "locations": [
                    "27086a67c269015eef3a02793f019508"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "remitly": CompanyConfig(
        api_url="https://remitly.wd5.myworkdayjobs.com/wday/cxs/remitly/Remitly_Careers/jobs",
        body={
            "appliedFacets": {
                "locationCountry": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ],
                "jobFamilyGroup": [
                    "c9699b32e2da1029a051260e906d0000"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": "Software+Developer"
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "openlane": CompanyConfig(
        api_url="https://kar.wd1.myworkdayjobs.com/wday/cxs/kar/OPENLANE_Careers/jobs",
        body={
            "appliedFacets": {
                "jobFamilyGroup": [
                    "1feabb51d74b0122d6b8a81cb700682d"
                ],
                "Location_Region_State_Province": [
                    "cb76ca97a13347548a188f23caa96b17"
                ],
                "Location_Country": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "weirmotors": CompanyConfig(
        api_url="https://weir.wd3.myworkdayjobs.com/wday/cxs/weir/Weir_External_Careers/jobs",
        body={
            "appliedFacets": {
                "Country": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ],
                "Region_State_Province": [
                    "cb76ca97a13347548a188f23caa96b17"
                ],
                "jobFamilyGroup": [
                    "c8ebc28620ef01501164ed0d01011278"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": "Software+Developer"
        }
    ),
    "accolade": CompanyConfig(
        api_url="https://osv-accolade.wd5.myworkdayjobs.com/wday/cxs/osv_accolade/External_Careers/jobs",
        body={
            "appliedFacets": {
                "jobFamilyGroup": [
                    "591060563623017f6db55ba7fd6b24f0"
                ],
                "primaryLocation": [
                    "2f2b3b9e18dc0199117b8d94ec01725e"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
    ),
    "workday": CompanyConfig(
        api_url="https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/jobs",
        body={
            "appliedFacets": {
                "jobFamilyGroup": [
                    "a88cba90a00841e0b750341c541b9d56",
                    "11d42f4a487c46b9b29ab3e087c2f5ca",
                    "8c5ce7a1cffb43e0a819c249a49fcb00"
                ],
                "locations": [
                    "2dbd309d3ef64fffb7131f8b596a774a"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "autodesk": CompanyConfig(
        api_url="https://autodesk.wd1.myworkdayjobs.com/wday/cxs/autodesk/Ext/jobs",
        body={
            "appliedFacets": {
                "locations": [
                    "dc0c7cba54ea1000a5a4d48e95d30000"
                ],
                "locationCountry": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ],
                "jobFamilyGroup": [
                    "1f75c4299c9201c0f3b5f8e6fa01c5bf"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "bcca": CompanyConfig(
        api_url="https://bcaa.wd3.myworkdayjobs.com/wday/cxs/bcaa/bcaacareers/jobs",
        body={
            "appliedFacets": {
                "jobFamilyGroup": [
                    "25ae589691dd01fe130456399749e007"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "flexera": CompanyConfig(
        api_url="https://flexerasoftware.wd1.myworkdayjobs.com/wday/cxs/flexerasoftware/FlexeraSoftware/jobs",
        body={
            "appliedFacets": {
                "locationCountry": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "ticketmaster": CompanyConfig(
        api_url="https://livenation.wd1.myworkdayjobs.com/wday/cxs/livenation/TMExternalSite/jobs",
        body={
            "appliedFacets": {
                "jobFamilyGroup": [
                    "def6fe28d9a210a6e1ddb30d81afbf0e"
                ],
                "Location_Country": [
                    "a30a87ed25634629aa6c3958aa2b91ea"
                ]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
        },
        job_age_key=JobPostingAgeKey.POSTED_ON
    ),
    "arcticwolf": CompanyConfig(
        api_url="https://arcticwolf.wd1.myworkdayjobs.com/wday/cxs/arcticwolf/External/jobs",
        body= {
        "appliedFacets": {
            "locations": [
                "f6cfbd603ca11001f6248a5f81c80000"
            ],
            "jobFamilyGroup": [
                "f6cfbd603ca11001ed8fdbe0fca80000"
            ]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
        },
        job_age_key="JobPostingAgeKey.POSTED_ON"
    ),

    # GREENHOUSE
    "take-two": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/taketwo/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published",
    ),
    "samsara": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/samsara/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "stripe": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/stripe/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "gitlab": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/gitlab/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "brex": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/brex/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "affinity": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/affinity/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "hootsuite": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/hootsuite/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "workleap": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/workleap/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "asana": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/asana/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "instacart": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/instacart/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "unbounce": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/unbounce/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "coalition": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/coalition/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "boomi": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/boomilp/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "leagueinc": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/leagueinc/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "shift4": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/shift4/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "benevity": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/benevity/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "launchpotato": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/launchpotato/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "earnin": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/earnin/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "destinationcanada": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/destinationcanada/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "workstream": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/workstream/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    "visier": CompanyConfig(
        api_url="https://boards-api.greenhouse.io/v1/boards/visiersolutionsinc/jobs",
        http_method="GET",
        parser_key="greenhouse",
        job_id_key="id",
        job_age_key="first_published"
    ),
    ### LEVER 
    "jane": CompanyConfig(
        api_url="https://api.lever.co/v0/postings/janeapp?location=Canada&team=Software%20Development",
        http_method="GET",
        parser_key="lever",
        job_id_key="text",
        job_age_key="createdAt"
    )
}

"""
 TODO: 
 - go through entire script

 """
