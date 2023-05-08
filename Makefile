#########
# BUILD #
#########
develop:  ## install dependencies and build library
	python3 -m pip install -e .[develop]
	python3 -m pip install pandas
	python3 -m pip install geopandas
	python3 -m pip install country-converter
	python3 -m pip install requests-mock
	python3 -m pip install matplotlib
	python3 -m pip install datetime

build:  ## build the python3 library
	python3 setup.py build build_ext --inplace

install:  ## install library
	python3 -m pip install .

#########
# LINTS #
#########
lint:  ## run static analysis with flake8
	python3 -m black --check epispread setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python3 -m black epispread/ setup.py

# alias
fix: format

check:  ## check assets for packaging
	check-manifest -v

# Alias
checks: check

annotate:  ## run type checking
	python3 -m mypy ./epispread

#########
# TESTS #
#########
test: ## clean and run unit tests
	python3 -m pytest -v epispread/tests

coverage:  ## clean and run unit tests with coverage
	python3 -m pytest -v epispread/tests --cov=epispread --cov-branch --cov-fail-under=75 --cov-report term-missing

# Alias
tests: test

###########
# VERSION #
###########
show-version:
	bump2version --dry-run --allow-dirty setup.py --list | grep current | awk -F= '{print $2}'

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

########
# DIST #
########
dist-build:  # Build python3 dist
	python3 setup.py sdist bdist_wheel

dist-check:
	python3 -m twine check dist/*

dist: clean build dist-build dist-check  ## Build dists

publish:  # Upload python3 assets
	echo "would usually run python3 -m twine upload dist/* --skip-existing"

#########
# CLEAN #
#########
deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info .pytest_cache

############################################################################################

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: develop build install lint lints format fix check checks annotate test coverage show-coverage tests show-version patch minor major dist-build dist-check dist publish deep-clean clean help

#########
# PAGES #
#########

TMPREPO=/tmp/docs/epispread
pages: 
	rm -rf $(TMPREPO)
	git clone -b gh-pages https://github.com/scb-school/epi-spread-visualizer.git $(TMPREPO)
	rm -rf $(TMPREPO)/*
	cp -r docs/_build/html/* $(TMPREPO)
	cd $(TMPREPO);\
	git add -A ;\
	git commit -a -m 'auto-updating docs' ;\
	git push
