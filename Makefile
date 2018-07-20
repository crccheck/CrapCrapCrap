help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

install: ## Install requirements
install: requirements.txt
	@[ -n "${VIRTUAL_ENV}" ] || (echo "ERROR: This should be run from a virtualenv" && exit 1)
	pip install -r requirements.txt

requirements.txt: ## Regenerate requirements.txt
requirements.txt: requirements.in
	pip-compile $< > $@

admin: ## Set up a local admin/admin account
	echo "from django.contrib.auth import get_user_model; \
	  User = get_user_model(); \
	  User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

clean:
	find . -type d -name "__pycache__" | xargs rm -rf

lint: ## Run lint check
	flake8
	node_modules/.bin/eslint --report-unused-disable-directives src/

dev: ## Run staticfiles watcher
	node_modules/.bin/watchify src/app.js --debug -o apps/tracker/static/app.js

build:
	node_modules/.bin/browserify src/app.js -o apps/tracker/static/app.js

test: ## Run test suite
	python manage.py test --noinput

tdd: ## Run test watcher
	nodemon -e py -x ./manage.py test --failfast --keepdb
