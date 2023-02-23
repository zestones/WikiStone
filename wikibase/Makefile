# Install the dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run the Flask app
.PHONY: wikistone
wikistone:
	flask --app wikibase_interface/main.py --debug run -h localhost -p 6060

# Run the wiki_injector script with arguments
.PHONY: inject
inject:
	- python3 wikibase_injector/main.py $(filter-out $@,$(MAKECMDGOALS))

# Clean up generated files
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +

# Print usage message
.PHONY: help
help:
	@echo "\033[35mUsage: make \033[1;32m<target>\033[0m\n"
	@echo "\033[1mTargets:\033[0m"
	@echo "\033[1m  install\033[0m      install the dependencies"
	@echo "\033[1m  wikistone\033[0m    run the Flask app"
	@echo "\033[1m  inject\033[0m       run the wiki_injector script with options\n"
	@echo "\033[34m  Options for \033[1minject:\033[0m"
	@echo "\033[1m   -- -h --help\033[0m    show the help message"
	@echo "\033[1m   -- -a --all\033[0m     process all data sources"
	@echo "\033[1m   -- -c --csv\033[0m     process csv data source"
	@echo "\033[1m   -- -j --json\033[0m    process json data source"
	@echo "\033[1m   -- -s --csv\033[0m     process data from Web Scraping"