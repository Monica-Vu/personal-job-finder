from enum import StrEnum
from typing import Set

# --- Constants ---
TIMESTAMP_MILLISECOND_THRESHOLD = 1_000_000_000_000
MILLISECONDS_PER_SECOND = 1000

# --- Enums ---
class JobPostingAgeKey(StrEnum):
    """Defines the API keys for a job's post date."""
    POSTED_ON = "postedOn"
    UPDATED_AT = "updated_at"

# --- Filtering Configuration ---
MAX_AGE_FOR_JOB_IN_DAYS: int = 3

# Terms to exclude from job searches 
TERMS_TO_EXCLUDE: Set[str] = {
    "STAFF", "SENIOR", "SR.", "SR", "MANAGER", "MOBILE",
    "MACHINE LEARNING", "MLOPS", "DEVOPS", "SALESFORCE",
    "DIRECTOR", "HELP DESK", "VP", "EXECUTIVE", "CO-OP",
    "COOP", "INTERN", "SALES", 'ASSISTANT', "SUPERVISOR",
    "RESEARCHER", "ANDROID", "HEAD", "LEAD", 'MANAGEMENT',
    "PRINCIPAL", "DESIGNER", "ARCHITECT", "DATA SCIENTIST", 
    "SCIENTIST", "STRATEGIST", "PRODUCT OWNER", "COMMUNICATIONS SPECIALIST"
}

# Locations to Include and Exclude 
LOCATION_KEY_WORDS = ["VANCOUVER", "BURNABY", "CANADA"]

EXCLUDE_LOCATION_KEY_WORDS = ["TORONTO", "MONTREAL",
                              "OTTAWA", "CALGARY", "ONTARIO", "ALBERTA", "QUEBEC"]

# path for job ids to exclude
APPLIED_JOBS_FILE = "excluded_jobs.json"

# TODO: think about the logic above more. Some places do list multiple offices or do "Remote Canada" (or something similar)