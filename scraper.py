# main.py
import requests
from models import JobPosting
import sys
import re
import json
import os
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone, timedelta
from company_configs import COMPANY_CONFIGS, CompanyConfig
from constants import EXCLUDE_LOCATION_KEY_WORDS, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS, APPLIED_JOBS_FILE, LOCATION_KEY_WORDS, TIMESTAMP_MILLISECOND_THRESHOLD, MILLISECONDS_PER_SECOND

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
        data_to_save = {company: list(
            job_ids) for company, job_ids in self.applied_ids_by_company.items()}
        try:
            with open(APPLIED_JOBS_FILE, 'w') as f:
                json.dump(data_to_save, f, indent=2)
            print(f"Successfully saved applied jobs to {APPLIED_JOBS_FILE}")
        except IOError as e:
            print(f"Error: Could not save applied jobs: {e}")

    def run(self, specific_companies: Optional[List[str]] = None):
        """Main method to run the entire scraping and filtering process."""
        companies_to_scrape = self.configs

        if specific_companies:
            companies_to_scrape = {
                name: config for name, config in self.configs.items()
                if name in specific_companies
            }

        print("--- Starting Job Scraper ---")
        all_jobs = self._fetch_and_parse_all_jobs(companies_to_scrape)

        print(f"\n--- Found {len(all_jobs)} total jobs. Filtering... ---")
        fresh_jobs = self._filter_jobs(all_jobs)

        if fresh_jobs:
            print(f"\n Found {len(fresh_jobs)} new, relevant jobs to review:")
            for job in fresh_jobs:
                print(
                    f"  - {job.title} at {job.company.title()} ({job.location}) | ID: {job.job_id}")
        else:
            print("\nNo new relevant jobs found.")

    def _fetch_and_parse_all_jobs(self, companies_to_scrape: Dict[str, CompanyConfig]) -> List[JobPosting]:
        all_parsed_jobs = []
        for name, config in companies_to_scrape.items():
            print(f"Fetching jobs for {name.title()}...")
            try:
                if config.http_method.upper() == "POST":
                    response = self.session.post(
                        config.api_url, json=config.body, timeout=10)
                else:
                    response = self.session.get(config.api_url, timeout=10)
                response.raise_for_status()

                json_data = response.json()
                
                if hasattr(config, 'data_path') and config.data_path: 
                    jobs_list = json_data
                    for key in config.data_path:
                        jobs_list = jobs_list[key]
                
                else: 
                    jobs_list = json_data

                parsed = self._parse_response(name, config, jobs_list)
                
                all_parsed_jobs.extend(parsed)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching jobs for {name.title()}: {e}")
        return all_parsed_jobs

    def _parse_response(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        """Routes to the correct parser based on the config's parser_key."""
        if config.parser_key == "workday":
            return self._parse_workday_jobs(company, config, data)
        elif config.parser_key == "greenhouse":
            return self._parse_greenhouse_jobs(company, config, data)
        elif config.parser_key == "lever":
            return self._parse_lever_jobs(company, config, data)
        elif config.parser_key == "ashbyhq": 
            return self._parse_ashbyhq_jobs(company, config, data)
        print(f"  No parser found for key: {config.parser_key}")
        return []

    def _parse_date(self, date_value: Optional[Any]) -> Optional[datetime]:
        parsed_date = self._parse_unix_timestamp(date_value)

        if parsed_date:
            return parsed_date

        if isinstance(date_value, str):
            return self._parse_iso_string(date_value) or self._parse_relative_string(date_value)

        return None

    def _parse_unix_timestamp(self, timestamp: Optional[Any]) -> Optional[datetime]:
        if timestamp is None:
            return None

        try:
            timestamp_float = float(timestamp)
        except (ValueError, TypeError):
            return None

        try:
            if timestamp_float > TIMESTAMP_MILLISECOND_THRESHOLD:
                timestamp_float /= MILLISECONDS_PER_SECOND
            return datetime.fromtimestamp(timestamp_float, tz=timezone.utc)

        except (ValueError, OSError):
            return None

    def _parse_iso_string(self, date_str: str) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None

    def _parse_relative_string(self, date_str: str) -> Optional[datetime]:
        date_str_lower = date_str.lower()
        if "today" in date_str_lower:
            return datetime.now(timezone.utc)
        if "yesterday" in date_str_lower:
            return datetime.now(timezone.utc) - timedelta(days=1)

        match = re.search(r'(\d+)\+?\s+days?\s+ago', date_str_lower)
        if match:
            return datetime.now(timezone.utc) - timedelta(days=int(match.group(1)))

        return None

    def _parse_workday_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        jobs = []
        for raw_job in data.get("jobPostings", []):
            job_id_list = raw_job.get(config.job_id_key, [])
            if not job_id_list:
                continue

            jobs.append(JobPosting(
                company=company,
                job_id=job_id_list[0],
                title=raw_job.get("title"),
                url=f"https://{config.api_url.split('/')[2]}{raw_job.get('externalPath', '')}",
                location=raw_job.get("locationsText"),
                posted_date=self._parse_date(raw_job.get(config.job_age_key))
            ))

        return jobs

    def _filter_jobs_by_location_fe(self, jobs, key):
        result = []

        included_areas = [kw.upper() for kw in LOCATION_KEY_WORDS]
        excluded_areas = [kw.upper() for kw in EXCLUDE_LOCATION_KEY_WORDS]

        keys = key.split('.')

        for raw_job in jobs:
            location_value = raw_job 

            try:
                for key in keys: 
                    location_value = location_value[key]
            except (KeyError, TypeError):
                location_value = ""
            
            location_name = str(location_value).upper()

            valid_locations = any(kw in location_name for kw in included_areas)
            invalid_locations = any(
                kw in location_name for kw in excluded_areas)

            if valid_locations and not invalid_locations:
                result.append(raw_job)
        return result
    
    def _filter_jobs_by_domain(self, jobs, key, target_domain_id): 
        result = []

        for job in jobs: 
            team_id = job[key]

            if (team_id == target_domain_id):
                result.append(job)
        
        return result


    def _parse_greenhouse_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        result = []
        jobs = data.get("jobs", [])
        location_relevant_jobs = self._filter_jobs_by_location_fe(jobs, key="locations.name")

        for raw_job in location_relevant_jobs:
            job_id = str(raw_job.get(config.job_id_key, ""))
            if not job_id:
                continue

            result.append(JobPosting(
                company=company,
                job_id=job_id,
                title=raw_job.get("title"),
                url=raw_job.get("absolute_url"),
                location=raw_job.get("location", {}).get("name"),
                posted_date=self._parse_date(raw_job.get(config.job_age_key))
            ))
        return result

    def _parse_lever_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        result = []

        for raw_job in data:
            result.append(JobPosting(
                company=company,
                job_id=raw_job.get("id"),
                title=raw_job.get("text"),
                url=raw_job.get("applyUrl"),
                location=raw_job.get("categories", {}).get("location"),
                posted_date=self._parse_date(raw_job.get(config.job_age_key))
            ))

        return result
    
    def _parse_ashbyhq_jobs(self, company: str, config: CompanyConfig, data: dict) -> List[JobPosting]:
        result = []
        location_relevant_jobs = self._filter_jobs_by_location_fe(data, key="locationName")
        domain_relevant_jobs = self._filter_jobs_by_domain(location_relevant_jobs, key="teamId", target_domain_id=config.team_id)

        for raw_job in domain_relevant_jobs:
            job_id = raw_job.get(config.job_id_key)
            if not job_id:
                continue
        
            result.append(JobPosting(
                company=company,
                job_id=raw_job.get(config.job_id_key),
                title=raw_job.get("title"),
                location=raw_job.get("locationName")
            ))

        return result

    def _is_relevant_title(self, title: Optional[str]) -> bool:
        if not title:
            return False

        title_upper = title.upper()
        to_exclude = any(term in title_upper for term in TERMS_TO_EXCLUDE)

        return not to_exclude

    def _filter_jobs(self, jobs: List[JobPosting]) -> List[JobPosting]:
        final_jobs = []
        today = datetime.now(timezone.utc)
        print("_filter_jobs is called")

        for job in jobs:
            if job.job_id in self.applied_ids_by_company.get(job.company, set()):
                continue
            if not self._is_relevant_title(job.title):
                continue
            if job.posted_date and (today - job.posted_date).days > MAX_AGE_FOR_JOB_IN_DAYS:
                continue

            final_jobs.append(job)

        return final_jobs


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company_list = sys.argv[1:]
    else:
        company_list = None

    scraper = JobScraper(COMPANY_CONFIGS)
    scraper.run(specific_companies=company_list)
