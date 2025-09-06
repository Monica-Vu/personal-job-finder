import re
import requests

APPLIED_JOBS = {}

TERMS_TO_EXCLUDE = set(["STAFF", "SENIOR", "MANAGER", "MOBILE", "MACHINE LEARNING", "MLOPS", "DEVOPS"])

MAX_AGE_FOR_JOB_IN_DAYS = 25

CLIO_JOBS_API_URL = "https://clio.wd3.myworkdayjobs.com/wday/cxs/clio/ClioCareerSite/jobs"

HEADERS = {
"User-Agent": "Job-Finder/1.0",
"Content-Type": "application/json"
}

# the following value is determined by the API
SEARCH_TEXT = "Software Developer"

# Locations ids can be found in the network tab for Workday 
LOCATION_IDS = [
"1b6969fbfbca0101f164999ecea20000",  # Vancouver, BC
"951c033a9bfe1000baf025938f160000"   # Remote, Canada
]

JOB_FAMILY_GROUP = ["29827a73287b0103383979088de50000"]

JOB_DISPLAY_LIMIT = 20 

def fetch_clio_jobs() -> None:
    print(
        f"Searching for '{SEARCH_TEXT} jobs in Vancouver or Remote, Canada for Clio")

    payload = {
        "appliedFacets": {
            "locations": LOCATION_IDS,
            "jobFamilyGroup": JOB_FAMILY_GROUP
        },
        "limit": JOB_DISPLAY_LIMIT,
        "offset": 0,
        "searchText": SEARCH_TEXT
    }

    try:
        response = requests.post(
            CLIO_JOBS_API_URL, headers=HEADERS, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        job_postings = data.get("jobPostings", [])
        return job_postings

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching from API: {e}")
        return


# TODO: write try catch statement and make sure jobPostings is a list object that's not empty
def find_fresh_relevant_jobs(jobPostings: list) -> None:
    relevant_jobs = []

    if not jobPostings:
        return "No object"
    
    for item in jobPostings:
        job_posted_days = int(extract_age_in_days(item))

        if (MAX_AGE_FOR_JOB_IN_DAYS > job_posted_days and include_job(item) and is_relevant_job(item)):
            relevant_jobs.append(item)

    return relevant_jobs


def extract_age_in_days(obj) -> None:
    # This regex looks for:
    # Posted          - The literal word "Posted"
    # \s+             - One or more whitespace characters
    # \d+\+?          - One or more digits (\d+), optionally followed by a plus sign (\+?)
    # \s+             - One or more whitespace characters
    # Days?           - The word "Day", with an optional "s" at the end
    # \s+             - One or more whitespace characters
    # Ago             - The literal word "Ago"
    # print("text =>", obj)
    text = obj.get("postedOn", "")

    if not text: 
        return "No date for error"    

    pattern = r"Posted\s+(\d+)\+?\s+Days?\s+Ago"

    match = re.search(pattern, text)

    if match:
        return match.group(1)
    
    return None 

def include_job(obj) -> bool:
    job_id = obj.get("bulletFields", "")

    if (job_id[0] in APPLIED_JOBS):
        return False
    return True

def is_relevant_job(obj) -> bool:
    job_title = obj.get("title", "")
    words_in_job_title = set(re.split(r'\W+', job_title.upper()))

    if TERMS_TO_EXCLUDE.intersection(words_in_job_title):
        return False 
    
    return True 

results = fetch_clio_jobs()
print(find_fresh_relevant_jobs(results))
