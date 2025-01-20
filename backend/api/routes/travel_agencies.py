# backend/api/routes/travel_agencies.py
from sanic import Blueprint, json
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.models.models import TravelAgency
from api.models.models import User
from api.models.models import Itinerary
from database import get_session

agencies_bp = Blueprint('agencies', url_prefix='/agencies')

@agencies_bp.get("/")
async def get_agencies(request):
    """List all travel agencies"""
    async with get_session() as session:
        query = select(TravelAgency).order_by(TravelAgency.name)
        result = await session.execute(query)
        agencies = result.scalars().all()
        
        return json([agency.to_dict(include_users=False) for agency in agencies])

@agencies_bp.get("/<agency_id:int>/users")
async def get_agency_users(request, agency_id):
    """List all users for a given travel agency"""
    async with get_session() as session:
        # Verify agency exists
        agency_result = await session.execute(
            select(TravelAgency).filter(TravelAgency.id == agency_id)
        )
        agency = agency_result.scalar_one_or_none()
        
        if not agency:
            return json({"error": "Travel agency not found"}, status=404)
        
        # Get users for agency without loading itineraries
        query = (
            select(User)
            .filter(User.travel_agency_id == agency_id)
            .order_by(User.name)
        )
        result = await session.execute(query)
        users = result.scalars().all()
        
        return json({
            "users": [user.to_dict(include_itineraries=False) for user in users]
        })

@agencies_bp.get("/users/<user_id:int>/itineraries")
async def get_user_itineraries(request, user_id):
    """List all itineraries for a given user with their trips and lodgings"""
    async with get_session() as session:
        # Verify user exists
        user_result = await session.execute(
            select(User).filter(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            return json({"error": "User not found"}, status=404)
        
        # Get itineraries with eager loading of trips and lodgings
        query = (
            select(Itinerary)
            .options(
                joinedload(Itinerary.trips),
                joinedload(Itinerary.lodgings)
            )
            .filter(Itinerary.user_id == user_id)
            .order_by(Itinerary.date_start)
        )
        
        result = await session.execute(query)
        itineraries = result.unique().scalars().all()
        
        return json({
            "itineraries": [
                itinerary.to_dict(include_relationships=True) 
                for itinerary in itineraries
            ]
        })

@agencies_bp.get("/itineraries/<itinerary_id:int>/details")
async def get_itinerary_details(request, itinerary_id):
    """List all lodging AND trips for a given itinerary"""
    async with get_session() as session:
        # Get itinerary with related trips and lodgings
        query = (
            select(Itinerary)
            .options(
                joinedload(Itinerary.trips),
                joinedload(Itinerary.lodgings)
            )
            .filter(Itinerary.id == itinerary_id)
        )
        result = await session.execute(query)
        itinerary = result.unique().scalar_one_or_none()
        
        if not itinerary:
            return json({"error": "Itinerary not found"}, status=404)
        
        # Format response
        return json({
            "itinerary": {
                "id": itinerary.id,
                "tour_name": itinerary.tour_name,
                "date_start": str(itinerary.date_start),
                "date_end": str(itinerary.date_end),
                "user_id": itinerary.user_id
            },
            "trips": [trip.to_dict() for trip in itinerary.trips],
            "lodgings": [lodging.to_dict() for lodging in itinerary.lodgings]
        })