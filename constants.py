"""
Constants and configuration values for the job scraper
"""

# Global state for tracking applied jobs
APPLIED_JOBS = {}

# Terms to exclude from job searches
TERMS_TO_EXCLUDE = set([
    "STAFF", 
    "SENIOR", 
    "MANAGER", 
    "MOBILE", 
    "MACHINE LEARNING", 
    "MLOPS", 
    "DEVOPS"
])

# Maximum age for jobs to be considered fresh (in days)
MAX_AGE_FOR_JOB_IN_DAYS = 25

# HTTP headers for API requests
HEADERS = {
    "User-Agent": "Job-Finder/1.0",
    "Content-Type": "application/json"
}
