# Job Scraper Unit Tests

This directory contains comprehensive unit tests for the job scraper module.

## Test Files

- `test_scraper.py` - Main test suite with unit tests for all scraper functions
- `run_tests.py` - Simple test runner script
- `requirements-test.txt` - Testing dependencies (optional, for pytest)

## Running Tests

### Using unittest (built-in)
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m unittest test_scraper -v

# Run specific test class
python -m unittest test_scraper.TestExtractAgeInDays -v

# Run specific test method
python -m unittest test_scraper.TestExtractAgeInDays.test_today -v
```

### Using the test runner script
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests using the custom runner
python run_tests.py
```

### Using pytest (optional)
```bash
# Install pytest first
pip install -r requirements-test.txt

# Run tests with pytest
pytest test_scraper.py -v

# Run with coverage
pytest test_scraper.py --cov=scraper --cov-report=html
```

## Test Coverage

The test suite covers:

### Core Functions
- ✅ `extract_age_in_days()` - Date parsing with various formats
- ✅ `include_job()` - Job application tracking
- ✅ `is_relevant_job()` - Job relevance filtering
- ✅ `find_fresh_relevant_jobs()` - Main job filtering logic

### API Functions
- ✅ `fetch_workday_jobs()` - API requests with mocking
- ✅ `search_jobs_for_company()` - Company-specific searches
- ✅ `search_jobs_for_all_companies()` - Multi-company searches

### Utility Functions
- ✅ `get_available_companies()` - Company configuration access
- ✅ `print_job_summary()` - Output formatting

## Test Categories

### TestExtractAgeInDays
- Tests date parsing for "Today", "Yesterday", and "Posted X Days Ago" formats
- Handles edge cases like missing dates and invalid formats

### TestIncludeJob
- Tests job application tracking
- Handles empty and missing bullet fields

### TestIsRelevantJob
- Tests job title filtering based on excluded terms
- Case-insensitive matching
- Handles empty and missing titles

### TestFindFreshRelevantJobs
- Tests the main job filtering pipeline
- Combines age, relevance, and application status checks
- Handles various edge cases and error conditions

### TestFetchWorkdayJobs
- Tests API interactions with mocked requests
- Handles successful responses, errors, and network issues
- Validates request payload construction

### TestSearchJobsForCompany & TestSearchJobsForAllCompanies
- Tests high-level search functions
- Integration testing with mocked dependencies

### TestPrintJobSummary
- Tests output formatting and summary generation

## Mocking Strategy

The tests use Python's `unittest.mock` to:
- Mock HTTP requests to avoid actual API calls
- Isolate units under test
- Test error handling scenarios
- Verify function interactions

## Test Data

Tests use realistic job posting data structures that match the expected Workday API response format:

```python
{
    "title": "Software Developer",
    "postedOn": "Posted 5 Days Ago",
    "bulletFields": ["job123"]
}
```

## Running Tests in CI/CD

For continuous integration, use:
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

This will discover and run all test files in the current directory.
