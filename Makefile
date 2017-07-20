# Minimal makefile for Sphinx documentation
#

# Documentation generator configuration
SPHINXBUILD   = python -msphinx
SPHINXOPTS    = "html"
SPHINXPROJ    = python-tmcl
SOURCEDIR     = ./docs
BUILDDIR      = ./docs/_build

.PHONY: docs Makefile


docs:
	@$(SPHINXBUILD) -j 4 -c ./docs -a "$(SOURCEDIR)" "$(BUILDDIR)"

