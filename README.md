# Personal Job Finder

A Python script that retrieves fresh, relevant jobs specific companies or organization that use Workday or Greenhouse. 

# Features
* Get all fresh and relevant jobs listed in the `company_configs.py` file OR a specific list company if passed via command line argument 

# How to Run
```
source venv/bin/activate && python3 scraper.py [optional list of arguments here]
```

## Examples 
```
source venv/bin/activate && python3 scraper.py
```

```
source venv/bin/activate && python3 scraper.py janeapp
```

```
# For multiple company key names, we seperate by spaces 
source venv/bin/activate && python3 scraper.py clio crowdstrike stripe hootsuite janeapp
```

# Future To-Do's 
* Run calls to fetch jobs in parallel 
* Automate the script to run once or twice every weekday and send email of all relevant jobs 
* 