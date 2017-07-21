
# Documentation generator configuration
############################################
SPHINXBUILD   = python -msphinx
SPHINXOPTS    = "html"
SPHINXPROJ    = python-tmcl
SOURCEDIR     = ./docs
BUILDDIR      = ./docs/_build


.PHONY: docs build Makefile


clean:
	rm -rf ./{build,dist}

build:	clean
	python setup.py sdist bdist_wheel


release-test:	build
	twine upload -r pypi-test dist/*

dev-dependencies:
	pip install -r requirements.dev.txt

test-dependencies:
	pip install -r requirements.test.txt

docs-dependencies:
	pip install -r requirements.docs.txt

dependencies: dev-dependencies test-dependencies docs-dependencies


tests:
	py.test test


docs:
	@$(SPHINXBUILD) -j 4 -c ./docs -a "$(SOURCEDIR)" "$(BUILDDIR)"

