# Workday Job Scraper

A generalized Python scraper for job postings from companies that use Workday's job board system.

## Features

- **Multi-company support**: Easily add new companies that use Workday
- **Configurable search parameters**: Customize search terms, locations, and job families per company
- **Smart filtering**: Automatically filters out irrelevant jobs and tracks applied positions
- **Company-aware job tracking**: Track applied jobs per company (same job ID can exist for different companies)
- **Error handling**: Robust error handling for API failures and data parsing issues
- **Flexible execution**: Search individual companies or all configured companies at once

## How to Add a New Company

To add a new company that uses Workday, follow these steps:

### 1. Find the Company's Workday API URL

1. Go to the company's careers page (e.g., `https://company.com/careers`)
2. Open your browser's Developer Tools (F12)
3. Go to the Network tab
4. Search for jobs on their website
5. Look for API calls to URLs containing `workdayjobs.com`
6. The URL will typically look like: `https://company.wd3.myworkdayjobs.com/wday/cxs/company/CareerSite/jobs`

### 2. Find Location and Job Family IDs

1. In the same Network tab, look at the POST request to the jobs API
2. Find the request payload (usually in the "Request" or "Payload" section)
3. Look for `appliedFacets` object containing:
   - `locations`: Array of location IDs
   - `jobFamilyGroup`: Array of job family IDs

### 3. Add Company Configuration

Add a new entry to the `COMPANY_CONFIGS` dictionary in `scraper.py`:

```python
"company_key": CompanyConfig(
    name="Company Display Name",
    api_url="https://company.wd3.myworkdayjobs.com/wday/cxs/company/CareerSite/jobs",
    search_text="Software Developer",  # or whatever search term you want
    location_ids=[
        "location_id_1",  # Found in step 2
        "location_id_2"
    ],
    job_family_group=["job_family_id"],  # Found in step 2
    job_display_limit=20
),
```

### Example: Adding a New Company

```python
COMPANY_CONFIGS = {
    "clio": CompanyConfig(
        name="Clio",
        api_url="https://clio.wd3.myworkdayjobs.com/wday/cxs/clio/ClioCareerSite/jobs",
        search_text="Software Developer",
        location_ids=[
            "1b6969fbfbca0101f164999ecea20000",  # Vancouver, BC
            "951c033a9bfe1000baf025938f160000"   # Remote, Canada
        ],
        job_family_group=["29827a73287b0103383979088de50000"],
        job_display_limit=20
    ),
    "new_company": CompanyConfig(
        name="New Company Inc",
        api_url="https://newcompany.wd3.myworkdayjobs.com/wday/cxs/newcompany/CareerSite/jobs",
        search_text="Software Engineer",
        location_ids=[
            "abc123def456",  # San Francisco, CA
            "xyz789uvw012"   # Remote, USA
        ],
        job_family_group=["def456ghi789"],
        job_display_limit=25
    ),
}
```

## Usage

### Search All Companies
```python
python scraper.py
```

### Search Specific Company
```python
# In your Python script or interactive session
results = search_jobs_for_company("clio")
print(results)
```

### Get Available Companies
```python
companies = get_available_companies()
print(companies)  # ['clio', 'new_company', ...]
```

## Job Tracking

The scraper includes company-aware job tracking to help you avoid applying to the same job multiple times. The key benefit is that **the same job ID can exist for different companies**, so you can apply to job "REQ-123" at both Clio and Remitly without conflicts.

### Mark Jobs as Applied
```python
# Mark a job as applied for a specific company
mark_job_as_applied("clio", "REQ-123")
mark_job_as_applied("remitly", "REQ-456")

# The same job ID can be applied to at different companies
mark_job_as_applied("clio", "REQ-789")
mark_job_as_applied("remitly", "REQ-789")  # This is allowed!
```

### Check Applied Jobs
```python
# Get applied jobs for a specific company
clio_applied = get_applied_jobs_for_company("clio")
print(clio_applied)  # ['REQ-123', 'REQ-789']

# Get all applied jobs across all companies
all_applied = get_all_applied_jobs()
print(all_applied)  # {'clio': ['REQ-123', 'REQ-789'], 'remitly': ['REQ-456', 'REQ-789']}
```

### Clear Applied Jobs
```python
# Clear applied jobs for a specific company
clear_applied_jobs_for_company("clio")

# Clear all applied jobs for all companies
clear_all_applied_jobs()
```

### How It Works
- Each company maintains its own list of applied job IDs
- The same job ID can exist for multiple companies
- When searching jobs, the scraper only excludes jobs you've applied to for that specific company
- This allows you to apply to the same job ID at different companies without conflicts
- **Applied jobs are saved persistently** in `applied_jobs.json` and persist between script runs
- The `applied_jobs.json` file is automatically created and managed by the scraper

## Configuration Options

### CompanyConfig Parameters

- `name`: Display name for the company
- `api_url`: Full Workday API URL for the company
- `search_text`: Search term to use (e.g., "Software Developer", "Data Scientist")
- `location_ids`: List of location IDs from Workday (found in browser dev tools)
- `job_family_group`: List of job family group IDs (found in browser dev tools)
- `job_display_limit`: Maximum number of jobs to fetch (default: 20)

### Global Settings

- `MAX_AGE_FOR_JOB_IN_DAYS`: Maximum age of jobs to consider (default: 25)
- `TERMS_TO_EXCLUDE`: Set of terms to exclude from job titles (e.g., "SENIOR", "MANAGER")
- `APPLIED_JOBS`: Dictionary to track jobs you've already applied to

## Troubleshooting

### Common Issues

1. **"Company not found in configuration"**
   - Make sure the company key exists in `COMPANY_CONFIGS`
   - Check for typos in the company key

2. **"Error while fetching from API"**
   - Verify the API URL is correct
   - Check if the company's Workday setup has changed
   - Ensure location and job family IDs are still valid

3. **"No job postings found"**
   - The search criteria might be too restrictive
   - Try different location IDs or job family groups
   - Check if the search text is appropriate for that company

### Finding Updated IDs

If a company's Workday setup changes, you may need to update the location and job family IDs:

1. Go to the company's careers page
2. Open Developer Tools → Network tab
3. Perform a job search
4. Look for the API request and extract new IDs from the payload

## Dependencies

- `requests`: For HTTP API calls
- `re`: For regex pattern matching (built-in)
- `typing`: For type hints (built-in)
- `dataclasses`: For configuration classes (built-in)

Install with:
```bash
pip install requests
```
