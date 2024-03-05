# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = 'SPremote'
copyright = '2024, Jens Flemming'
author = 'Jens Flemming'
version = ''
release = '0.0'

extensions = ['myst_parser', 'autodoc2']
myst_enable_extensions = ['fieldlist']

autodoc2_packages = ['../../spremote']
autodoc2_render_plugin = 'myst'
autodoc2_module_all_regexes = [r'.*']  # follow __all__ in all files
autodoc2_class_docstring = 'merge'  # no separate __init__ section
autodoc2_skip_module_regexes = ['.*']  # skip all modules
autodoc2_hidden_objects = ['dunder', 'private']  # don't show dunden and private things
autodoc2_index_template = None  # don't create index.rst

exclude_patterns = ['apidocs']

myst_heading_anchors = 4

html_static_path = ['_static']
html_theme = 'sphinx_book_theme'

