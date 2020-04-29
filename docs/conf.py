"""Sphinx configuration."""
from datetime import datetime


project = "poetry-merge-lock"
author = "Claudio Jolowicz"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
