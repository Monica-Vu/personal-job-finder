"""
Constants and configuration values for the job scraper
"""

import json
import os

# File to store applied jobs persistently
APPLIED_JOBS_FILE = "applied_jobs.json"

# Global state for tracking applied jobs per company
# Structure: {company_key: {job_id: True, ...}}
APPLIED_JOBS = {}

def load_applied_jobs():
    """Load applied jobs from persistent storage"""
    global APPLIED_JOBS
    if os.path.exists(APPLIED_JOBS_FILE):
        try:
            with open(APPLIED_JOBS_FILE, 'r') as f:
                APPLIED_JOBS = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load applied jobs from {APPLIED_JOBS_FILE}: {e}")
            APPLIED_JOBS = {}
    else:
        APPLIED_JOBS = {}

def save_applied_jobs():
    """Save applied jobs to persistent storage"""
    try:
        with open(APPLIED_JOBS_FILE, 'w') as f:
            json.dump(APPLIED_JOBS, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save applied jobs to {APPLIED_JOBS_FILE}: {e}")

# Load applied jobs on module import
load_applied_jobs()

# Terms to exclude from job searches
TERMS_TO_EXCLUDE = set([
    "STAFF", 
    "SENIOR", 
    "SR.",  # Added Sr. abbreviation
    "MANAGER", 
    "MOBILE", 
    "MACHINE LEARNING",  # Keep as exact phrase
    "MLOPS", 
    "DEVOPS",
    "SALESFORCE"  # Added Salesforce
])

# Maximum age for jobs to be considered fresh (in days)
MAX_AGE_FOR_JOB_IN_DAYS: int = 3

# HTTP headers for API requests
HEADERS = {
    "User-Agent": "Job-Finder/1.0",
    "Content-Type": "application/json"
}
