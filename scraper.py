import re
import requests
from typing import Dict, List, Optional, Any
from constants import APPLIED_JOBS, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS, HEADERS, save_applied_jobs
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

    # Build appliedFacets dynamically based on configuration
    applied_facets = {
        config.location_facet_key: config.location_ids,
        config.job_family_facet_key: config.job_family_group
    }
    
    # Add locationCountry facet if configured (for companies like Remitly)
    if config.location_country_ids:
        applied_facets[config.location_country_facet_key] = config.location_country_ids

    payload = {
        "appliedFacets": applied_facets,
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


def find_fresh_relevant_jobs(job_postings: List[Dict[str, Any]], company_name: str = "", company_key: str = "") -> List[Dict[str, Any]]:
    """
    Filter job postings to find fresh, relevant jobs
    
    Args:
        job_postings: List of job posting dictionaries
        company_name: Name of the company for logging purposes
        company_key: Company key for tracking applied jobs per company
        
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
                include_job(item, company_key) and 
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
    text = obj.get("postedOn", "")

    if not text: 
        return "No date for error" 

    if text == "Posted Today":
        return 0

    if text == "Posted Yesterday":
        return 1   

    pattern = r"Posted\s+(\d+)\+?\s+Days?\s+ago"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1)
    
    return None 

def include_job(obj: Dict[str, Any], company_key: str) -> bool:
    """
    Check if a job should be included based on whether it's already been applied to
    
    Args:
        obj: Job posting object
        company_key: Company key from COMPANY_CONFIGS
        
    Returns:
        True if job should be included, False if already applied to
    """
    job_id = obj.get("bulletFields", [])

    if not job_id or len(job_id) == 0:
        return True
    
    # Check if this job ID has been applied to for this specific company
    if company_key in APPLIED_JOBS and job_id[0] in APPLIED_JOBS[company_key]:
        return False
    
    return True

def is_relevant_job(obj) -> bool:
    job_title = obj.get("title", "").upper()
    
    # Check for exact phrase matches first (like "MACHINE LEARNING")
    for excluded_term in TERMS_TO_EXCLUDE:
        if excluded_term in job_title:
            return False
    
    return True 

def get_available_companies() -> List[str]:
    """Return list of available company keys"""
    return list(COMPANY_CONFIGS.keys())

def mark_job_as_applied(company_key: str, job_id: str) -> None:
    """
    Mark a job as applied to for a specific company
    
    Args:
        company_key: Company key from COMPANY_CONFIGS
        job_id: Job ID from the job posting
    """
    if company_key not in APPLIED_JOBS:
        APPLIED_JOBS[company_key] = {}
    
    APPLIED_JOBS[company_key][job_id] = True
    save_applied_jobs()  # Save to persistent storage
    print(f"Marked job {job_id} as applied for {COMPANY_CONFIGS[company_key].name}")

def get_applied_jobs_for_company(company_key: str) -> List[str]:
    """
    Get list of applied job IDs for a specific company
    
    Args:
        company_key: Company key from COMPANY_CONFIGS
        
    Returns:
        List of job IDs that have been applied to
    """
    if company_key not in APPLIED_JOBS:
        return []
    
    return list(APPLIED_JOBS[company_key].keys())

def get_all_applied_jobs() -> Dict[str, List[str]]:
    """
    Get all applied jobs organized by company
    
    Returns:
        Dictionary mapping company keys to lists of applied job IDs
    """
    return {company_key: list(jobs.keys()) for company_key, jobs in APPLIED_JOBS.items()}

def clear_applied_jobs_for_company(company_key: str) -> None:
    """
    Clear all applied jobs for a specific company
    
    Args:
        company_key: Company key from COMPANY_CONFIGS
    """
    if company_key in APPLIED_JOBS:
        del APPLIED_JOBS[company_key]
        save_applied_jobs()  # Save to persistent storage
        print(f"Cleared all applied jobs for {COMPANY_CONFIGS[company_key].name}")

def clear_all_applied_jobs() -> None:
    """Clear all applied jobs for all companies"""
    APPLIED_JOBS.clear()
    save_applied_jobs()  # Save to persistent storage
    print("Cleared all applied jobs for all companies")

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
    return find_fresh_relevant_jobs(job_postings, config.name, company_key)

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
