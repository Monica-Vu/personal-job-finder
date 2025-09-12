from company_configs import COMPANY_CONFIGS
from constants import HEADERS, JobPostingAgeKey, JobFreshness, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS
import requests
import re

def get_jobs_from_company(company: str) -> list or None:
    obj = COMPANY_CONFIGS[company]

    try: 
        response = requests.post(obj.api_url, headers=HEADERS, json=obj.body, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        job_postings = data.get("jobPostings", [])
        return job_postings
    
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching from {company}'s API: {e}")
        return None

def find_fresh_relevant_jobs(job_postings: list, company: str):
    obj = COMPANY_CONFIGS[company]
    relevant_jobs = []

    job_posted_days = 0

    for item in job_postings: 
        if obj.job_age_key == JobPostingAgeKey.POSTED_ON:
            job_posted_days = extract_days_of_job_posting(item)
        
        if MAX_AGE_FOR_JOB_IN_DAYS > job_posted_days and include_job(item) and is_relevant_job(item):
            relevant_jobs.append(item)
    
    return relevant_jobs

def extract_days_of_job_posting(job):
    date_string = job.get("postedOn", "").casefold()

    if not date_string:
        return "A falsey value is returned in `extract_days_of_job_postings`"

    if date_string == JobFreshness.TODAY.casefold():
        return 0

    if date_string == JobFreshness.YESTERDAY.casefold():
        return 1 
    
    pattern = r"Posted\s+(\d+)\+?\s+Days?\s+ago"

    match = re.search(pattern, date_string, re.IGNORECASE)

    if match:
        return int(match.group(1))
    
    return None 

def include_job(obj: any):
    job_id = obj.get("bulletFields", [])

    return job_id

def is_relevant_job(obj) -> bool:
    job_title = obj.get("title", "").upper()
    words_in_title = set(re.split(r'\W+', job_title.upper()))

    return not TERMS_TO_EXCLUDE.intersection(words_in_title)

def find_workday_jobs():
    results = []

    for company in COMPANY_CONFIGS:
        all_jobs = get_jobs_from_company(company)
        relevant_jobs = find_fresh_relevant_jobs(all_jobs, company)
        results.extend(relevant_jobs)
    
    return results



# results = get_jobs_from_company("clio")
# print(find_fresh_relevant_jobs(results, "clio"))

print(find_workday_jobs())