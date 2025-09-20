.PHONY: install lint test 

install:
		pip install -r requirements.txt 
		pip install -r requirements-dev.txt
	
lint: 
		ruff check . 