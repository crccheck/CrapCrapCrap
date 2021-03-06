TARGET_URL ?= https://www.amazon.com/dp/B07LDNGG6J

help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

install: ## Install requirements
install:
	@[ -n "${VIRTUAL_ENV}" ] || [ -f ".python-version" ] || (echo "ERROR: This should be run from a virtualenv" && exit 1)
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
	node_modules/.bin/eslint --report-unused-disable-directives src/ browser_ext/popup

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
build: browser_ext/browser-polyfill.js
	node_modules/.bin/browserify src/app.js -o apps/tracker/static/app.js
	node_modules/.bin/sass src/app.scss:apps/tracker/static/app.css --no-source-map

# BROWSER EXTENSION

web-ext: ## Terminal 1: Start web-ext for browser extension
web-ext: browser_ext/browser-polyfill.js browser_ext/manifest.json
	cd browser_ext && web-ext run --url $(TARGET_URL)

ext/dev: ## Terminal 2: Start dev watcher for browser extension
ext/dev: browser_ext/browser-polyfill.js browser_ext/manifest.json
	node_modules/.bin/concurrently \
	  --names "background,crap,manifest,test" \
	  "${MAKE} ext/dev/browser_ext/background.js" \
	  "${MAKE} ext/dev/browser_ext/crap.js" \
	  "${MAKE} ext/dev/browser_ext/manifest.json" \
	  "${MAKE} ext/tdd"

browser_ext/browser-polyfill.js: node_modules/webextension-polyfill/dist/browser-polyfill.min.js
	cp $< $@

ext/dev/browser_ext/background.js:
	node_modules/.bin/watchify -t [ envify purge --NODE_ENV development ] src/extension/background.js -o browser_ext/background.js

ext/dev/browser_ext/crap.js:
	node_modules/.bin/watchify -t [ envify purge --NODE_ENV development ] src/extension/crap.js -o browser_ext/crap.js

ext/dev/browser_ext/manifest.json:
	nodemon -w "src/extension/manifest.json" -x "make browser_ext/manifest.json"

browser_ext/manifest.json: src/extension/manifest.json package.json
	node src/extension/manifest_build.js > browser_ext/manifest.json

ext/tdd:
	node_modules/.bin/mocha src/**/*.spec.js --watch --watch-files=src

ext/test:
	node_modules/.bin/mocha src/**/*.spec.js

# Pick a new version and set it in package.json
# git checkout master
# git pull
# update package.json with the next version
# Update CHANGELOG
# git commit -am $(jq -r .version package.json)
# make ext/build # this takes 1 to 2.5 minutes
# amend HEAD if necessary
# TODO: do releases with a pull request
# git tag v$(jq -r .version package.json)
# git push --follow-tags
ext/build: ## Build browser extension artifact
	NODE_ENV=production ${MAKE} -s browser_ext/manifest.json
	node_modules/.bin/browserify -t [ envify purge --NODE_ENV production ] src/extension/crap.js -o browser_ext/crap.js
	node_modules/.bin/browserify -t [ envify purge --NODE_ENV production ] src/extension/background.js -o browser_ext/background.js
	cd browser_ext && web-ext build && web-ext sign --api-key=${AMO_JWT_ISSUER} --api-secret=${AMO_JWT_SECRET} --channel=unlisted
	@echo Submit it at https://addons.mozilla.org/en-US/developers/addons
	@echo and at https://chrome.google.com/webstore/developer/dashboard

ext/publish: ## Publish browser extension XPI
	rsync -avz browser_ext/web-ext-artifacts/*.xpi dh:addons.craptobuy.com/downloads
	@echo View it at https://addons.craptobuy.com/downloads/
