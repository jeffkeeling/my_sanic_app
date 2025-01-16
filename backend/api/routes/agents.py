# backend/api/routes/agents.py
from sanic import Blueprint, json
from sqlalchemy.future import select
from database import get_session
from api.models.models import TravelAgent

agents_bp = Blueprint('agents', url_prefix='/agents')

@agents_bp.get("/")
async def get_agents(request):
    """Get all agents with pagination"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    async with get_session() as session:
        # Get total count
        count_result = await session.execute(select(func.count(TravelAgent.id)))
        total = count_result.scalar()
        
        # Get paginated results
        result = await session.execute(
            select(TravelAgent)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        agents = result.scalars().all()
        
        # Build response with HATEOAS links
        response = {
            "data": [agent.to_dict() for agent in agents],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            },
            "_links": {
                "self": f"/api/agents?page={page}&per_page={per_page}",
                "next": f"/api/agents?page={page+1}&per_page={per_page}" if page * per_page < total else None,
                "prev": f"/api/agents?page={page-1}&per_page={per_page}" if page > 1 else None
            }
        }
        return json(response)

@agents_bp.get("/<agent_id:int>")
async def get_agent(request, agent_id):
    """Get a specific agent"""
    async with get_session() as session:
        result = await session.execute(
            select(TravelAgent).filter(TravelAgent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            return json({"error": "Agent not found"}, status=404)
            
        # Include HATEOAS links
        response = {
            "data": agent.to_dict(),
            "_links": {
                "self": f"/api/agents/{agent_id}",
                "collection": "/api/agents",
                "agencies": f"/api/agencies?agent_id={agent_id}"
            }
        }
        return json(response)

@agents_bp.post("/")
async def create_agent(request):
    """Create a new agent"""
    data = request.json
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email']
    if not all(field in data for field in required_fields):
        return json({
            "error": "Missing required fields",
            "required_fields": required_fields
        }, status=400)
    
    async with get_session() as session:
        agent = TravelAgent(**data)
        session.add(agent)
        try:
            await session.commit()
            response = {
                "data": agent.to_dict(),
                "_links": {
                    "self": f"/api/agents/{agent.id}",
                    "collection": "/api/agents"
                }
            }
            # 201 Created for successful resource creation
            return json(response, status=201, headers={
                'Location': f"/api/agents/{agent.id}"
            })
        except IntegrityError:
            await session.rollback()
            return json({"error": "Email already exists"}, status=409)

@agents_bp.put("/<agent_id:int>")
async def update_agent(request, agent_id):
    """Update an existing agent"""
    data = request.json
    async with get_session() as session:
        result = await session.execute(
            select(TravelAgent).filter(TravelAgent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            return json({"error": "Agent not found"}, status=404)
        
        # Update fields
        for key, value in data.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        try:
            await session.commit()
            return json({
                "data": agent.to_dict(),
                "_links": {
                    "self": f"/api/agents/{agent.id}",
                    "collection": "/api/agents"
                }
            })
        except IntegrityError:
            await session.rollback()
            return json({"error": "Email already exists"}, status=409)

@agents_bp.delete("/<agent_id:int>")
async def delete_agent(request, agent_id):
    """Delete an agent"""
    async with get_session() as session:
        result = await session.execute(
            select(TravelAgent).filter(TravelAgent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            return json({"error": "Agent not found"}, status=404)
        
        await session.delete(agent)
        await session.commit()
        # 204 No Content for successful deletion
        return json({}, status=204)