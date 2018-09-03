CrapCrapCrap
============

[![Build Status](https://travis-ci.org/crccheck/CrapCrapCrap.svg?branch=master)](https://travis-ci.org/crccheck/CrapCrapCrap)

Run your own price tracker, similar to CamelCamelCamel.


Release process
---------------

### Site

Wait for CI to build the Docker image and deploy that

### Browser extension

1. Manually bump `package.json` version
2. `make ext/build` and follow the instructions
3. `make ext/publish` to make it available
4. `git commit -am $(cat package.json | jq -r .version)`
5. `git tag v$(cat package.json | jq -r .version)`
6. `git push origin master --tags`
