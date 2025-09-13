# main.py
import requests
import re
import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set
from company_configs import COMPANY_CONFIGS, CompanyConfig
# Import from our other  project files
from constants import EXCLUDE_LOCATION_KEY_WORDS, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS, APPLIED_JOBS_FILE, LOCATION_KEY_WORDS
from models import JobPosting

# --- Main Application Class ---
class JobScraper:
    def __init__(self, configs: dict):
        self.configs = configs
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "MyJobScraper/1.0"})
        self.applied_ids_by_company = self._load_applied_jobs()

    def _load_applied_jobs(self) -> Dict[str, Set[str]]:
        """Loads applied job IDs from the JSON file."""
        if not os.path.exists(APPLIED_JOBS_FILE):
            return {}
        try:
            with open(APPLIED_JOBS_FILE, 'r') as f:
                raw_data = json.load(f)
                return {company: set(job_ids) for company, job_ids in raw_data.items()}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load applied jobs file: {e}")
            return {}

    def save_applied_jobs(self):
        """Saves the current state of applied jobs to the JSON file."""
        data_to_save = {company: list(job_ids) for company, job_ids in self.applied_ids_by_company.items()}
        try:
            with open(APPLIED_JOBS_FILE, 'w') as f:
                json.dump(data_to_save, f, indent=2)
            print(f"✅ Successfully saved applied jobs to {APPLIED_JOBS_FILE}")
        except IOError as e:
            print(f"❌ Error: Could not save applied jobs: {e}")

    def run(self):
        """Main method to run the entire scraping and filtering process."""
        print("--- Starting Job Scraper ---")
        all_jobs = self._fetch_and_parse_all_jobs()
        
        print(f"\n--- Found {len(all_jobs)} total jobs. Filtering... ---")
        fresh_jobs = self._filter_jobs(all_jobs)

        if fresh_jobs:
            print(f"\n Found {len(fresh_jobs)} new, relevant jobs to review:")
            for job in fresh_jobs:
                print(f"  - {job.title} at {job.company.title()} ({job.location})")
        else:
            print("\nNo new relevant jobs found.")

    def _fetch_and_parse_all_jobs(self) -> List[JobPosting]:
        all_parsed_jobs = []
        for name, config in self.configs.items():
            print(f"Fetching jobs for {name.title()}...")
            try:
                if config.http_method.upper() == "POST":
                    response = self.session.post(config.api_url, json=config.body, timeout=10)
                else:
                    response = self.session.get(config.api_url, timeout=10)
                response.raise_for_status()
                
                parsed = self._parse_response(name, config, response.json())
                all_parsed_jobs.extend(parsed)
            except requests.exceptions.RequestException as e:
                print(f"  ❌ Error fetching jobs for {name.title()}: {e}")
        return all_parsed_jobs

    def _parse_response(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        """Routes to the correct parser based on the config's parser_key."""
        if config.parser_key == "workday":
            return self._parse_workday_jobs(company, config, data)
        elif config.parser_key == "greenhouse":
            return self._parse_greenhouse_jobs(company, config, data)
        print(f"  No parser found for key: {config.parser_key}")
        return []

    def _parse_date(self, date_value: Optional[str]) -> Optional[datetime]:
        """Parses a date that can be an ISO timestamp or a relative string."""
        if not isinstance(date_value, str): return None
        try:
            return datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        except ValueError:
            date_str_lower = date_value.lower()
            if "today" in date_str_lower: return datetime.now(timezone.utc)
            if "yesterday" in date_str_lower: return datetime.now(timezone.utc) - timedelta(days=1)
            match = re.search(r'(\d+)\+?\s+days?\s+ago', date_str_lower)
            if match: return datetime.now(timezone.utc) - timedelta(days=int(match.group(1)))
        return None

    def _parse_workday_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        jobs = []
        for raw_job in data.get("jobPostings", []):
            job_id_list = raw_job.get(config.job_id_key, [])
            if not job_id_list: continue
            
            jobs.append(JobPosting(
                company=company,
                job_id=job_id_list[0],
                title=raw_job.get("title"),
                url=f"https://{config.api_url.split('/')[2]}{raw_job.get('externalPath', '')}",
                location=raw_job.get("locationsText"),
                posted_date=self._parse_date(raw_job.get(config.job_age_key))
            ))

        return jobs
    
    def _filter_gh_jobs_by_location(self, jobs):
        result = []

        included_areas = [kw.upper() for kw in LOCATION_KEY_WORDS]
        excluded_areas = [kw.upper() for kw in EXCLUDE_LOCATION_KEY_WORDS]

        for raw_job in jobs: 
            location_name = raw_job.get('location', {}).get('name','').upper()

            valid_locations = any(kw in location_name for kw in included_areas)
            invalid_locations = any(kw in location_name for kw in excluded_areas)

            if valid_locations and not invalid_locations:
                result.append(raw_job)
        return result 

    def _parse_greenhouse_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        result = []
        jobs = data.get("jobs", [])
        location_relevant_jobs = self._filter_gh_jobs_by_location(jobs)

        for raw_job in location_relevant_jobs:
            job_id = str(raw_job.get(config.job_id_key, ""))
            if not job_id: continue

            result.append(JobPosting(
                company=company,
                job_id=job_id,
                title=raw_job.get("title"),
                url=raw_job.get("absolute_url"),
                location=raw_job.get("location", {}).get("name"),
                posted_date=self._parse_date(raw_job.get(config.job_age_key))
            ))
        return result

    def _is_relevant_title(self, title: Optional[str]) -> bool:
        """Efficiently checks if a title contains excluded terms using uppercase."""
        if not title: return False
        # Using .upper() as you prefer
        words_in_title = set(re.split(r'\W+', title.upper()))
        return not TERMS_TO_EXCLUDE.intersection(words_in_title)

    def _filter_jobs(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """Filters a list of JobPosting objects through a pipeline of checks."""
        final_jobs = []
        today = datetime.now(timezone.utc)
        
        for job in jobs:
            if job.job_id in self.applied_ids_by_company.get(job.company, set()):
                continue
            if not self._is_relevant_title(job.title):
                continue
            # This logic now KEEPS jobs with no date
            if job.posted_date and (today - job.posted_date).days > MAX_AGE_FOR_JOB_IN_DAYS:
                continue
            
            final_jobs.append(job)
                
        return final_jobs

if __name__ == "__main__":
    scraper = JobScraper(COMPANY_CONFIGS)
    scraper.run()