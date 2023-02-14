# Install the dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run the Flask app
.PHONY: wikistone
wikistone:
	flask --app wikibase_interface/main.py --debug run

# Run the wiki_injector script
.PHONY: inject
inject:
	python3 wikibase_injector/main.py