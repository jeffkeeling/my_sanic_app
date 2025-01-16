# backend/api/routes/__init__.py
"""
This file initializes all route blueprints and groups them together.
"""

from sanic import Blueprint
from .users import users_bp
from .lodgings import lodgings_bp
from .itineraries import itineraries_bp
from .trips import trips_bp
# Import other blueprints as you create them
# from .auth import auth_bp
# from .products import products_bp

# Group all API routes under /api prefix
api = Blueprint.group(
    users_bp,
    lodgings_bp,
	itineraries_bp,
	trips_bp,
    # auth_bp,
    # products_bp,
    url_prefix='/api'
)