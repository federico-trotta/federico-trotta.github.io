# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'Portfolio'
copyright = '2023, Federico Trotta'
author = 'Federico Trotta'
release = '0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # For Furo's own documentation
    "furo.sphinxext",
    # Myst parser
    "myst_parser",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = "Federico Trotta's portfolio"
myst_enable_extensions = ["colon_fence"] # For admonitions (read also: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-colon-fence)
myst_number_code_blocks = ["python"] # Numbering lines in code blocks (read also: https://myst-parser.readthedocs.io/en/latest/syntax/code_and_apis.html)



# Deploy tutorial: https://medium.com/practical-coding/documenting-your-python-library-from-zero-to-website-488f87ae58f5