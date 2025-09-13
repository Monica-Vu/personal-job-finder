jobs = 
    {
      "absolute_url": "https://job-boards.greenhouse.io/unbounce/jobs/4891627008",
      "data_compliance": [
        {
          "type": "gdpr",
          "requires_consent": false,
          "requires_processing_consent": false,
          "requires_retention_consent": false,
          "retention_period": null,
          "demographic_data_consent_applies": false
        }
      ],
      "internal_job_id": 4326871008,
      "location": {
        "name": "Remote, Canada and US"
      },
      "metadata": null,
      "id": 4891627008,
      "updated_at": "2025-08-21T12:26:51-04:00",
      "requisition_id": "27",
      "title": "Fullstack Software Developer",
      "company_name": "Unbounce",
      "first_published": "2025-08-20T16:11:11-04:00"
    },
    {
      "absolute_url": "https://job-boards.greenhouse.io/unbounce/jobs/4838399008",
      "data_compliance": [
        {
          "type": "gdpr",
          "requires_consent": false,
          "requires_processing_consent": false,
          "requires_retention_consent": false,
          "retention_period": null,
          "demographic_data_consent_applies": false
        }
      ],
      "internal_job_id": 4306930008,
      "location": {
        "name": "Remote, Canada and US"
      },
      "metadata": null,
      "id": 4838399008,
      "updated_at": "2025-09-12T17:33:16-04:00",
      "requisition_id": "24",
      "title": "Infrastructure Developer",
      "company_name": "Unbounce",
      "first_published": "2025-08-05T14:24:50-04:00"
    }
    ]"

def filter_response(response):
    response.filter(lambda object)

print(filter_response(jobs))