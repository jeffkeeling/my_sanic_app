# backend/api/__init__.py
"""
This file makes the api directory a Python package.
It can be empty, but often contains package-level configuration or imports.
"""

from sanic import Sanic

def init_app(app: Sanic) -> None:
    """Initialize the API package with the Sanic app instance."""
    # You can add any API-wide configuration here
    pass