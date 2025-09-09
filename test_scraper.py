"""
Unit tests for the job scraper module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper import (
    fetch_workday_jobs,
    find_fresh_relevant_jobs,
    extract_age_in_days,
    include_job,
    is_relevant_job,
    get_available_companies,
    search_jobs_for_company,
    search_jobs_for_all_companies,
    print_job_summary
)
from constants import APPLIED_JOBS, TERMS_TO_EXCLUDE, MAX_AGE_FOR_JOB_IN_DAYS
from company_configs import COMPANY_CONFIGS


class TestExtractAgeInDays(unittest.TestCase):
    """Test the extract_age_in_days function"""
    
    def test_today(self):
        """Test handling of 'Posted Today' date"""
        job = {"postedOn": "Posted Today"}
        result = extract_age_in_days(job)
        self.assertEqual(result, 0)
    
    def test_yesterday(self):
        """Test handling of 'Posted Yesterday' date"""
        job = {"postedOn": "Posted Yesterday"}
        result = extract_age_in_days(job)
        self.assertEqual(result, 1)
    
    def test_posted_days_ago(self):
        """Test parsing of 'Posted X Days ago' format"""
        test_cases = [
            ("Posted 5 Days ago", "5"),
            ("Posted 5 days ago", "5"),  # lowercase 'days'
            ("Posted 1 Day ago", "1"),
            ("Posted 1 day ago", "1"),   # lowercase 'day'
            ("Posted 10+ Days ago", "10"),
            ("Posted 30 Days ago", "30")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                job = {"postedOn": input_text}
                result = extract_age_in_days(job)
                self.assertEqual(result, expected)
    
    def test_no_date(self):
        """Test handling of missing or empty date"""
        test_cases = [
            {"postedOn": ""},
            {"postedOn": None},
            {}
        ]
        
        for job in test_cases:
            with self.subTest(job=job):
                result = extract_age_in_days(job)
                self.assertEqual(result, "No date for error")
    
    def test_invalid_date_format(self):
        """Test handling of invalid date formats"""
        job = {"postedOn": "Invalid date format"}
        result = extract_age_in_days(job)
        self.assertIsNone(result)


class TestIncludeJob(unittest.TestCase):
    """Test the include_job function"""
    
    def setUp(self):
        """Set up test data"""
        # Clear APPLIED_JOBS for each test
        APPLIED_JOBS.clear()
    
    def test_job_not_applied(self):
        """Test job that hasn't been applied to"""
        job = {"bulletFields": ["job123"]}
        result = include_job(job)
        self.assertTrue(result)
    
    def test_job_already_applied(self):
        """Test job that has already been applied to"""
        job = {"bulletFields": ["job123"]}
        APPLIED_JOBS["job123"] = True
        result = include_job(job)
        self.assertFalse(result)
    
    def test_empty_bullet_fields(self):
        """Test job with empty bullet fields"""
        job = {"bulletFields": []}
        result = include_job(job)
        self.assertTrue(result)
    
    def test_missing_bullet_fields(self):
        """Test job with missing bullet fields"""
        job = {}
        result = include_job(job)
        self.assertTrue(result)


class TestIsRelevantJob(unittest.TestCase):
    """Test the is_relevant_job function"""
    
    def test_relevant_job(self):
        """Test job with relevant title"""
        job = {"title": "Software Developer"}
        result = is_relevant_job(job)
        self.assertTrue(result)
    
    def test_excluded_terms(self):
        """Test jobs with excluded terms"""
        excluded_titles = [
            "Senior Software Developer",
            "Staff Engineer",
            "Mobile Developer",
            "Machine Learning Engineer",
            "MLOps Engineer",
            "DevOps Engineer",
            "Engineering Manager"
        ]
        
        for title in excluded_titles:
            with self.subTest(title=title):
                job = {"title": title}
                result = is_relevant_job(job)
                self.assertFalse(result, f"Job with title '{title}' should be excluded")
    
    def test_individual_words_not_excluded(self):
        """Test that individual words like 'Machine' or 'Learning' are not excluded"""
        allowed_titles = [
            "Machine Operator",
            "Learning Specialist", 
            "Machine Shop Worker",
            "Learning and Development Coordinator"
        ]
        
        for title in allowed_titles:
            with self.subTest(title=title):
                job = {"title": title}
                result = is_relevant_job(job)
                self.assertTrue(result, f"Job with title '{title}' should be allowed")
    
    def test_case_insensitive_exclusion(self):
        """Test that exclusion is case insensitive"""
        job = {"title": "senior software developer"}
        result = is_relevant_job(job)
        self.assertFalse(result)
    
    def test_empty_title(self):
        """Test job with empty title"""
        job = {"title": ""}
        result = is_relevant_job(job)
        self.assertTrue(result)
    
    def test_missing_title(self):
        """Test job with missing title"""
        job = {}
        result = is_relevant_job(job)
        self.assertTrue(result)


class TestFindFreshRelevantJobs(unittest.TestCase):
    """Test the find_fresh_relevant_jobs function"""
    
    def setUp(self):
        """Set up test data"""
        APPLIED_JOBS.clear()
    
    def test_empty_job_list(self):
        """Test with empty job list"""
        result = find_fresh_relevant_jobs([], "Test Company")
        self.assertEqual(result, [])
    
    def test_non_list_input(self):
        """Test with non-list input"""
        result = find_fresh_relevant_jobs("not a list", "Test Company")
        self.assertEqual(result, [])
    
    def test_fresh_relevant_job(self):
        """Test finding a fresh, relevant job"""
        job = {
            "title": "Software Developer",
            "postedOn": "Posted 5 Days ago",
            "bulletFields": ["job123"]
        }
        result = find_fresh_relevant_jobs([job], "Test Company")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], job)
    
    def test_old_job_excluded(self):
        """Test that old jobs are excluded"""
        job = {
            "title": "Software Developer",
            "postedOn": "Posted 30 Days ago",  # Older than MAX_AGE_FOR_JOB_IN_DAYS
            "bulletFields": ["job123"]
        }
        result = find_fresh_relevant_jobs([job], "Test Company")
        self.assertEqual(len(result), 0)
    
    def test_irrelevant_job_excluded(self):
        """Test that irrelevant jobs are excluded"""
        job = {
            "title": "Senior Software Developer",  # Contains excluded term
            "postedOn": "Posted 5 Days ago",
            "bulletFields": ["job123"]
        }
        result = find_fresh_relevant_jobs([job], "Test Company")
        self.assertEqual(len(result), 0)
    
    def test_applied_job_excluded(self):
        """Test that already applied jobs are excluded"""
        job = {
            "title": "Software Developer",
            "postedOn": "Posted 5 Days ago",
            "bulletFields": ["job123"]
        }
        APPLIED_JOBS["job123"] = True
        result = find_fresh_relevant_jobs([job], "Test Company")
        self.assertEqual(len(result), 0)
    
    def test_job_with_invalid_date(self):
        """Test job with invalid date format"""
        job = {
            "title": "Software Developer",
            "postedOn": "Invalid date",
            "bulletFields": ["job123"]
        }
        result = find_fresh_relevant_jobs([job], "Test Company")
        self.assertEqual(len(result), 0)
    
    def test_mixed_jobs(self):
        """Test with mix of relevant and irrelevant jobs"""
        jobs = [
            {
                "title": "Software Developer",
                "postedOn": "Posted 5 Days ago",
                "bulletFields": ["job1"]
            },
            {
                "title": "Senior Developer",  # Excluded
                "postedOn": "Posted 3 Days ago",
                "bulletFields": ["job2"]
            },
            {
                "title": "Junior Developer",
                "postedOn": "Posted 30 Days ago",  # Too old
                "bulletFields": ["job3"]
            },
            {
                "title": "Frontend Developer",
                "postedOn": "Posted 2 Days ago",
                "bulletFields": ["job4"]
            }
        ]
        result = find_fresh_relevant_jobs(jobs, "Test Company")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Software Developer")
        self.assertEqual(result[1]["title"], "Frontend Developer")


class TestGetAvailableCompanies(unittest.TestCase):
    """Test the get_available_companies function"""
    
    def test_returns_company_keys(self):
        """Test that function returns list of company keys"""
        result = get_available_companies()
        self.assertIsInstance(result, list)
        self.assertIn("clio", result)
        self.assertIn("crowdstrike", result)


class TestFetchWorkdayJobs(unittest.TestCase):
    """Test the fetch_workday_jobs function"""
    
    @patch('scraper.requests.post')
    def test_successful_fetch(self, mock_post):
        """Test successful job fetching"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "jobPostings": [
                {"title": "Software Developer", "postedOn": "Posted 5 Days ago"},
                {"title": "Frontend Developer", "postedOn": "Posted 3 Days ago"}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = fetch_workday_jobs("clio")
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Software Developer")
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], COMPANY_CONFIGS["clio"].api_url)
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")
    
    def test_invalid_company_key(self):
        """Test with invalid company key"""
        result = fetch_workday_jobs("nonexistent_company")
        self.assertIsNone(result)
    
    @patch('scraper.requests.post')
    def test_request_exception(self, mock_post):
        """Test handling of request exceptions"""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        result = fetch_workday_jobs("clio")
        self.assertIsNone(result)
    
    @patch('scraper.requests.post')
    def test_empty_job_postings(self, mock_post):
        """Test response with empty job postings"""
        mock_response = Mock()
        mock_response.json.return_value = {"jobPostings": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = fetch_workday_jobs("clio")
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)


class TestSearchJobsForCompany(unittest.TestCase):
    """Test the search_jobs_for_company function"""
    
    @patch('scraper.fetch_workday_jobs')
    def test_successful_search(self, mock_fetch):
        """Test successful job search for a company"""
        mock_jobs = [
            {
                "title": "Software Developer",
                "postedOn": "Posted 5 Days ago",
                "bulletFields": ["job1"]
            }
        ]
        mock_fetch.return_value = mock_jobs
        
        result = search_jobs_for_company("clio")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Software Developer")
        mock_fetch.assert_called_once_with("clio")
    
    @patch('scraper.fetch_workday_jobs')
    def test_fetch_returns_none(self, mock_fetch):
        """Test when fetch_workday_jobs returns None"""
        mock_fetch.return_value = None
        
        result = search_jobs_for_company("clio")
        
        self.assertEqual(result, [])
        mock_fetch.assert_called_once_with("clio")


class TestSearchJobsForAllCompanies(unittest.TestCase):
    """Test the search_jobs_for_all_companies function"""
    
    @patch('scraper.search_jobs_for_company')
    def test_search_all_companies(self, mock_search):
        """Test searching all companies"""
        mock_search.side_effect = [
            [{"title": "Clio Job"}],
            [{"title": "CrowdStrike Job"}]
        ]
        
        result = search_jobs_for_all_companies()
        
        self.assertIn("clio", result)
        self.assertIn("crowdstrike", result)
        self.assertEqual(len(result["clio"]), 1)
        self.assertEqual(len(result["crowdstrike"]), 1)
        self.assertEqual(mock_search.call_count, 2)


class TestPrintJobSummary(unittest.TestCase):
    """Test the print_job_summary function"""
    
    @patch('builtins.print')
    def test_print_summary(self, mock_print):
        """Test that job summary is printed correctly"""
        all_results = {
            "clio": [
                {"title": "Software Developer"},
                {"title": "Frontend Developer"}
            ],
            "crowdstrike": [
                {"title": "Security Engineer"}
            ]
        }
        
        print_job_summary(all_results)
        
        # Verify that print was called multiple times
        self.assertGreater(mock_print.call_count, 0)
        
        # Check that company names and job counts are printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        summary_text = " ".join(print_calls)
        
        self.assertIn("Clio: 2 relevant jobs", summary_text)
        self.assertIn("CrowdStrike: 1 relevant jobs", summary_text)
        self.assertIn("Total relevant jobs found: 3", summary_text)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
