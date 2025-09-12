# constants.py
from enum import StrEnum
from typing import Set

# --- Enums ---
class JobPostingAgeKey(StrEnum):
    """Defines the API keys for a job's post date."""
    POSTED_ON = "postedOn"
    UPDATED_AT = "updated_at"

# --- Filtering Configuration ---
MAX_AGE_FOR_JOB_IN_DAYS: int = 25

# Terms to exclude from job searches (in uppercase, as you prefer)
TERMS_TO_EXCLUDE: Set[str] = {
    "STAFF", "SENIOR", "SR.", "MANAGER", "MOBILE", 
    "MACHINE LEARNING", "MLOPS", "DEVOPS", "SALESFORCE",
    "DIRECTOR", "HELP DESK"
}

# --- File paths ---
APPLIED_JOBS_FILE = "excluded_jobs.json"