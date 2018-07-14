help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

install: ## Install requirements
	@[ -n "${VIRTUAL_ENV}" ] || (echo "ERROR: This should be run from a virtualenv" && exit 1)
	pip install -r requirements.txt

requirements.txt: ## Regenerate requirements.txt
requirements.txt: requirements.in
	pip-compile $< > $@

lint: ## Run lint check
	flake8

test: ## Run test suite
test: lint
	python manage.py test --noinput

tdd: ## Run test watcher
	nodemon -e py -x ./manage.py test --failfast --keepdb
