from __future__         import unicode_literals
from javaproperties_cli import __version__

project   = 'javaproperties-cli'
author    = 'John T. Wodder II'
copyright = '2016-2020 John T. Wodder II'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

autodoc_default_flags = ['members', 'undoc-members']

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "javaproperties": ("https://javaproperties.readthedocs.io/en/latest", None),
}

exclude_patterns = ['_build']
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
version = __version__
release = __version__
today_fmt = '%Y %b %d'
default_role = 'py:obj'
pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    "collapse_navigation": False,
}
html_last_updated_fmt = '%Y %b %d'
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
