import re
import requests
from typing import Dict, List, Optional, Any
from constants import APPLIED_JOBS, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS, HEADERS
from company_configs import COMPANY_CONFIGS 

def fetch_workday_jobs(company_key: str) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch job postings from a company's Workday API
    
    Args:
        company_key: Key from COMPANY_CONFIGS dictionary
        
    Returns:
        List of job postings or None if error
    """
    if company_key not in COMPANY_CONFIGS:
        print(f"Error: Company '{company_key}' not found in configuration")
        return None
    
    config = COMPANY_CONFIGS[company_key]
    
    print(f"Searching for '{config.search_text}' jobs for {config.name}")

    payload = {
        "appliedFacets": {
            config.location_facet_key: config.location_ids,
            config.job_family_facet_key: config.job_family_group
        },
        "limit": config.job_display_limit,
        "offset": 0,
        "searchText": config.search_text
    }

    try:
        response = requests.post(
            config.api_url, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        job_postings = data.get("jobPostings", [])
        print(f"Found {len(job_postings)} total jobs for {config.name}")
        return job_postings

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching from {config.name} API: {e}")
        return None


def find_fresh_relevant_jobs(job_postings: List[Dict[str, Any]], company_name: str = "") -> List[Dict[str, Any]]:
    """
    Filter job postings to find fresh, relevant jobs
    
    Args:
        job_postings: List of job posting dictionaries
        company_name: Name of the company for logging purposes
        
    Returns:
        List of relevant job postings
    """
    relevant_jobs = []

    if not job_postings:
        print(f"No job postings found for {company_name}")
        return relevant_jobs
    
    if not isinstance(job_postings, list):
        print(f"Error: Expected list of job postings, got {type(job_postings)}")
        return relevant_jobs
    
    for item in job_postings:
        try:
            job_posted_days = extract_age_in_days(item)
            
            if job_posted_days is None:
                print(f"Warning: Could not extract job age for job: {item.get('title', 'Unknown')}")
                continue
                
            job_posted_days = int(job_posted_days)

            if (MAX_AGE_FOR_JOB_IN_DAYS > job_posted_days and 
                include_job(item) and 
                is_relevant_job(item)):
                relevant_jobs.append(item)
                
        except (ValueError, TypeError) as e:
            print(f"Error processing job posting: {e}")
            continue

    print(f"Found {len(relevant_jobs)} relevant jobs for {company_name}")
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

    if text == "Today":
        return 0

    if text == "Yesterday":
        return 1   

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

def get_available_companies() -> List[str]:
    """Return list of available company keys"""
    return list(COMPANY_CONFIGS.keys())

def search_jobs_for_company(company_key: str) -> List[Dict[str, Any]]:
    """
    Search for jobs for a specific company
    
    Args:
        company_key: Key from COMPANY_CONFIGS dictionary
        
    Returns:
        List of relevant job postings
    """
    job_postings = fetch_workday_jobs(company_key)
    if job_postings is None:
        return []
    
    config = COMPANY_CONFIGS[company_key]
    return find_fresh_relevant_jobs(job_postings, config.name)

def search_jobs_for_all_companies() -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for jobs across all configured companies
    
    Returns:
        Dictionary mapping company keys to their relevant job postings
    """
    all_results = {}
    
    for company_key in COMPANY_CONFIGS.keys():
        print(f"\n{'='*50}")
        print(f"Searching {COMPANY_CONFIGS[company_key].name}")
        print(f"{'='*50}")
        
        results = search_jobs_for_company(company_key)
        all_results[company_key] = results
    
    return all_results

def print_job_summary(all_results: Dict[str, List[Dict[str, Any]]]) -> None:
    """Print a summary of all job search results"""
    print(f"\n{'='*60}")
    print("JOB SEARCH SUMMARY")
    print(f"{'='*60}")
    
    total_jobs = 0
    for company_key, jobs in all_results.items():
        company_name = COMPANY_CONFIGS[company_key].name
        print(f"{company_name}: {len(jobs)} relevant jobs")
        total_jobs += len(jobs)
        
        # Print job titles
        for job in jobs:
            print(f"  - {job.get('title', 'Unknown Title')}")
    
    print(f"\nTotal relevant jobs found: {total_jobs}")

# Main execution
if __name__ == "__main__":
    # Example usage - search all companies
    all_results = search_jobs_for_all_companies()
    print_job_summary(all_results)
    
    # Example usage - search specific company
    # results = search_jobs_for_company("clio")
    # print(f"Clio results: {results}")
