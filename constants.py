# constants.py
from enum import StrEnum
from typing import Set

# --- Enums ---
class JobPostingAgeKey(StrEnum):
    """Defines the API keys for a job's post date."""
    POSTED_ON = "postedOn"
    UPDATED_AT = "updated_at"

# --- Filtering Configuration ---
MAX_AGE_FOR_JOB_IN_DAYS: int = 3

# Terms to exclude from job searches (in uppercase, as you prefer)
TERMS_TO_EXCLUDE: Set[str] = {
    "STAFF", "SENIOR", "SR.", "MANAGER", "MOBILE", 
    "MACHINE LEARNING", "MLOPS", "DEVOPS", "SALESFORCE",
    "DIRECTOR", "HELP DESK", "VP", "EXECUTIVE", "CO-OP", 
    "COOP", "INTERN", "SALES", 'ASSISTANT', "SUPERVISOR",
    "RESEARCHER", "ANDROID"
}

# --- File paths ---
APPLIED_JOBS_FILE = "excluded_jobs.json"

LOCATION_KEY_WORDS = ["VANCOUVER", "BURNABY", "CANADA"]

EXCLUDE_LOCATION_KEY_WORDS = ["TORONTO", "MONTREAL", "OTTAWA", "CALGARY", "ONTARIO", "ALBERTA", "QUEBEC"]