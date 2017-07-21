
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

docs:
	@$(SPHINXBUILD) -j 4 -c ./docs -a "$(SOURCEDIR)" "$(BUILDDIR)"

