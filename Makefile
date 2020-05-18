# Makefile for VA.gov performance dashboard
# Tested with GNU Make 3.8.1
MAKEFLAGS += --warn-undefined-variables
SHELL        	:= /usr/bin/env bash -e
CI_ARG      	:= $(CI)

.DEFAULT_GOAL := help

# cribbed from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html and https://news.ycombinator.com/item?id=11195539
help:  ## Prints out documentation for available commands
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST)

### Yarn / Node / etc.
# Simple solution per https://stackoverflow.com/questions/44036997/how-to-prevent-yarn-install-from-running-twice-in-makefile (fold option)
# This will not detect if node_modules has been messed with however.
node_modules:
	mkdir -p $@

yarn.lock: node_modules package.json
ifeq ($(CI_ARG), true)
	yarn install --frozen-lockfile --non-interactive
else
	yarn install --check-files
endif
	touch $@

.PHONY: copy-node-dependencies
copy-node-dependencies: yarn.lock
	mkdir -p src/assets/vendor/chart.js
	cp node_modules/chart.js/dist/Chart.bundle.min.js src/assets/vendor/chart.js/
	mkdir -p src/assets/vendor/formation/sass
# The "*" after /dist/ is important here, as BSD vs GNU treats the semantics differently if you don't have the *
	cp -r node_modules/@department-of-veterans-affairs/formation/dist/* src/assets/vendor/formation/
	cp -r node_modules/@department-of-veterans-affairs/formation/sass/* src/assets/vendor/formation/sass/

.PHONY: yarn-install
yarn-install: yarn.lock copy-node-dependencies ## Install dependencies using yarn, copy some files to the src/assets/vendor directory

### Jekyll
.PHONY: build
build: yarn-install  ## Build the Jekyll site
	docker run --rm --volume=${PWD}:/srv/jekyll -it jekyll/jekyll:4.0  jekyll build --trace

.PHONY: run
run: yarn-install  ## Build the Jekyll site and start the Jekyll webserver on port 4000
	docker run --rm -p 4000:4000 --volume=${PWD}:/srv/jekyll -it jekyll/jekyll:4.0  jekyll serve --trace

## Pip / Python

.PHONY: python-install
# python-install recipe all has to run in a single shell because it's running inside a virtualenv
python-install:  ## Sets up your python environment for the first time (only need to run once)
	pip install virtualenv ;\
	virtualenv -p ~/.pyenv/shims/python ENV ;\
	source ENV/bin/activate ;\
	echo shell ENV activated ;\
	pip install --require-hashes -r scripts/requirements.txt -r scripts/dev-requirements.txt ;\
	echo Finished install ;\
	echo Please activate the virtualenvironment with: ;\
	echo source ENV/bin/activate

# Errors out if VIRTUAL_ENV is not defined and we aren't in a CI environment.
.PHONY: check-env
check-env:
ifndef VIRTUAL_ENV
ifneq ($(CI_ARG), true)
	$(error VIRTUAL_ENV is undefined, meaning you aren't running in a virtual environment. Fix by running: 'source ENV/bin/activate')
endif
endif

scripts/requirements.txt: scripts/requirements.in
	pip-compile --generate-hashes scripts/requirements.in --output-file $@

scripts/dev-requirements.txt: scripts/dev-requirements.in
	pip-compile --generate-hashes scripts/dev-requirements.in --output-file $@

.PHONY: pip-upgrade
pip-upgrade:  ## Upgrade all python dependencies
	pip-compile --upgrade --generate-hashes scripts/requirements.in --output-file scripts/requirements.txt
	pip-compile --upgrade --generate-hashes scripts/dev-requirements.in --output-file scripts/dev-requirements.txt

SITE_PACKAGES := $(shell pip show pip | grep '^Location' | cut -f2 -d ':')
$(SITE_PACKAGES): scripts/requirements.txt scripts/dev-requirements.txt check-env
ifeq ($(CI_ARG), true)
	@echo "Do nothing; assume python dependencies were installed by Dockerfile.test already"
else
	pip-sync scripts/requirements.txt scripts/dev-requirements.txt
endif

.PHONY: pip-install
pip-install: $(SITE_PACKAGES)

## Data fetch targets
.PHONY: fetch-data-local
fetch-data-local: pip-install
	cd scripts; ./fetch-data-local.sh

## Test targets
.PHONY: unit-test
unit-test: pip-install  ## Run python unit tests
	PYTHONWARNINGS='ignore::DeprecationWarning:numpy' \
	python -m pytest -v --cov --cov-report term --cov-report xml --cov-report html

.PHONY: flake8
flake8: pip-install 	## Run Flake8 python static style checking and linting
	@echo "flake8 comments:"
	flake8 --max-line-length=120 --statistics scripts

.PHONY: ci-unit-test
ci-unit-test:  CONTAINER_NAME := dashboard-test-container-$(shell date "+%Y.%m.%d-%H.%M.%S")
ci-unit-test:  ## Run unit tests and flake8 in a docker container, copy the results back out
	docker build -q -t dashboard-test-img -f Dockerfile.test .
	docker run --name $(CONTAINER_NAME) --env CI=$(CI_ARG) dashboard-test-img
	docker cp $(CONTAINER_NAME):/dashboard/results .
	docker rm $(CONTAINER_NAME)

.PHONY: ui-test
ui-test: build   ## Run UI tests nightwatch, chromedriver and chrome
	yarn run ui-test-headless

.PHONY: ci-ui-test
ci-ui-test:    ## Run UI tests nightwatch, chromedriver and chrome in CI without jekyll-build
	yarn run ui-test-headless

.PHONY: integration-test
integration-test: pip-install  ## Run data integration test
	cd scripts; INTEGRATION_TEST=TRUE ./fetch-data-docker-wrapper.sh

.PHONY: test
test: unit-test flake8 ui-test integration-test  ## Run unit tests, static analysis, integration, and ui tests
	@echo "All tests passed."  # This should only be printed if all of the other targets succeed

## Sonarqube
# Bring up sonar and wait a bit for it to start
.PHONY: sonar-up
sonar-up: ## Start sonarqube local containers
	result=`docker ps | grep sonarqube | wc -l`; \
	if [ $$result -eq 0 ]; then \
		docker-compose -f local-dev/sonar/docker-compose.yml up --detach; \
		echo "Waiting for 45 seconds..."; \
		sleep 45; \
	else\
		echo "Sonarqube already up"; \
	fi;

.PHONY: sonar-down
sonar-down: ## Stop sonarqube local containers
	docker-compose -f local-dev/sonar/docker-compose.yml down

.PHONY: sonar-start
sonar-scan: sonar-up unit-test ## Perform the sonar scan. This will start sonarqube if it needs to.
	mvn sonar:sonar
	open http://localhost:9000/dashboard?id=gov.va%3Aperformancedashboard

.PHONY: clean
clean:  ## Delete any directories, files or logs that are auto-generated, except node_modules and python packages
	rm -rf target
	rm -rf results
	rm -rf .pytest_cache
	rm -rf _site
	rm -f .coverage
	rm -rf src/.jekyll-cache
	rm -rf src/assets/vendor
	rm -rf test/ui/logs
	find scripts/data ! -name '.keep' -type f -exec rm -f {} +
	find scripts -name '__pycache__' -type d | xargs rm -rf

.PHONY: deepclean
deepclean: clean  ## Delete node_modules, python packages and virtualenv. You must run 'make python-install' after running this.
	rm -rf node_modules
	rm -rf ENV
	@echo virtualenvironment was deleted. Type 'deactivate' to deactivate the shims.
