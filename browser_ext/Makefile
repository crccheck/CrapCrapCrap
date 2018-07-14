help: ## Shows this help
	@echo "$$(grep -h '#\{2\}' $(MAKEFILE_LIST) | sed 's/: #\{2\} /	/' | column -t -s '	')"

dev: ## Start a dev browser
	web-ext run --url https://www.bigbadtoystore.com/Search?HideSoldOut=true&InventoryStatus=sa%2Ci%2Cp&SortOrder=Bestselling

lint: ## Check lint
	web-ext lint
