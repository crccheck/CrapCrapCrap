help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

install: ## Install requirements
install:
	@[ -n "${VIRTUAL_ENV}" ] || (echo "ERROR: This should be run from a virtualenv" && exit 1)
	pip install -r requirements.txt

.PHONY: requirements.txt
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

test: ## Run test suite
	env $$(cat example.env | xargs) python manage.py test --noinput

tdd: ## Run test watcher
	nodemon -e py -x ./manage.py test --failfast --keepdb

dev: ## Start dev server
	@${MAKE} -s -j dev/js dev/css dev/browser-sync dev/django

dev/django:
	python manage.py runserver 0.0.0.0:35272

dev/css:
	node_modules/.bin/sass src/app.scss:apps/tracker/static/app.css --embed-source-map --watch

dev/js:
	node_modules/.bin/watchify src/app.js --debug -o apps/tracker/static/app.js

dev/browser-sync:
	node_modules/.bin/browser-sync start --proxy localhost:35272 \
	  --no-open --no-ui --no-notify \
	  --files "apps/tracker/static/*"

build: ## Do a production build of static assets
	node_modules/.bin/browserify src/app.js -o apps/tracker/static/app.js
	node_modules/.bin/sass src/app.scss:apps/tracker/static/app.css --no-source-map

# BROWSER EXTENSION

ext/dev: ## Start dev process for browser extension
ext/dev: browser_ext/manifest.json
	cd browser_ext && web-ext run --url https://www.bigbadtoystore.com/Search?HideSoldOut=true&InventoryStatus=sa%2Ci%2Cp&SortOrder=Bestselling
	${MAKE} -j ext/dev/browser_ext/background.js ext/dev/browser_ext/crap.js ext/dev/browser_ext/manifest.json

ext/dev/browser_ext/background.js:
	node_modules/.bin/watchify -t [ envify purge --NODE_ENV development ] src/extension/background.js -o browser_ext/background.js

ext/dev/browser_ext/crap.js:
	node_modules/.bin/watchify -t [ envify purge --NODE_ENV development ] src/extension/crap.js -o browser_ext/crap.js

ext/dev/browser_ext/manifest.json:
	nodemon -w "src/extension/manifest.json" -x "make browser_ext/manifest.json"

browser_ext/manifest.json: src/extension/manifest.json package.json
	node src/extension/build_manifest.js > browser_ext/manifest.json

ext/build: ## Build browser extension artifact
	NODE_ENV=production ${MAKE} -s browser_ext/manifest.json
	node_modules/.bin/browserify -t [ envify purge --NODE_ENV production ] src/extension/crap.js -o browser_ext/crap.js
	node_modules/.bin/browserify -t [ envify purge --NODE_ENV production ] src/extension/background.js -o browser_ext/background.js
	cd browser_ext && web-ext build
	@echo Submit it at https://addons.mozilla.org/en-US/developers/addons

ext/publish: ## Publish browser extension XPI
	rsync -avz browser_ext/web-ext-artifacts/*.xpi dh:addons.craptobuy.com/downloads
	@echo View it at https://addons.craptobuy.com/downloads/
