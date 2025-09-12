# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class JobPosting:
    """A standardized representation of a single job posting."""
    # Required fields we need for filtering and identification
    company: str
    job_id: str
    
    # Optional fields that might be missing from an API response
    title: Optional[str] = "No Title Provided"
    location: Optional[str] = "N/A"
    url: Optional[str] = None
    posted_date: Optional[datetime] = None