# backend/api/routes/routes.py
from sanic import Blueprint, json
from sqlalchemy.future import select
from datetime import datetime
from database import get_session
from api.models.models import TravelAgent, TravelAgency, Itinerary, Trip, Lodging
import logging

logger = logging.getLogger(__name__)

# Create Blueprints
agents_bp = Blueprint('agents', url_prefix='/agents')
agencies_bp = Blueprint('agencies', url_prefix='/agencies')
itineraries_bp = Blueprint('itineraries', url_prefix='/itineraries')
trips_bp = Blueprint('trips', url_prefix='/trips')
lodgings_bp = Blueprint('lodgings', url_prefix='/lodgings')

# Helper function to parse dates
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

# Travel Agents Routes
@agents_bp.get("/")
async def get_agents(request):
    async with get_session() as session:
        try:
            result = await session.execute(select(TravelAgent))
            agents = result.scalars().all()
            return json([agent.to_dict() for agent in agents])
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            return json({"error": "Failed to fetch agents"}, status=500)

@agents_bp.post("/")
async def create_agent(request):
    data = request.json
    required_fields = ['first_name', 'last_name', 'email']
    if not all(field in data for field in required_fields):
        return json({"error": "Missing required fields"}, status=400)
    
    async with get_session() as session:
        try:
            agent = TravelAgent(**data)
            session.add(agent)
            await session.commit()
            return json(agent.to_dict(), status=201)
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating agent: {e}")
            return json({"error": "Failed to create agent"}, status=500)

@agents_bp.put("/<agent_id:int>")
async def update_agent(request, agent_id):
    data = request.json
    async with get_session() as session:
        try:
            result = await session.execute(
                select(TravelAgent).filter(TravelAgent.id == agent_id)
            )
            agent = result.scalar_one_or_none()
            if not agent:
                return json({"error": "Agent not found"}, status=404)
            
            for key, value in data.items():
                setattr(agent, key, value)
            
            await session.commit()
            return json(agent.to_dict())
        except Exception as e:
            await session.rollback()
            logger.error(f"Error updating agent: {e}")
            return json({"error": "Failed to update agent"}, status=500)

@agents_bp.delete("/<agent_id:int>")
async def delete_agent(request, agent_id):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(TravelAgent).filter(TravelAgent.id == agent_id)
            )
            agent = result.scalar_one_or_none()
            if not agent:
                return json({"error": "Agent not found"}, status=404)
            
            await session.delete(agent)
            await session.commit()
            return json({"message": "Agent deleted successfully"})
        except Exception as e:
            await session.rollback()
            logger.error(f"Error deleting agent: {e}")
            return json({"error": "Failed to delete agent"}, status=500)

# Similar CRUD routes for other models...
# (TravelAgency, Itinerary, Trip, and Lodging follow the same pattern)

# Create blueprint group
api = Blueprint.group(
    agents_bp,
    agencies_bp,
    itineraries_bp,
    trips_bp,
    lodgings_bp,
    url_prefix='/api'
)