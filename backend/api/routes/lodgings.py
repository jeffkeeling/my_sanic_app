# backend/api/routes/lodgings.py
from sanic import Blueprint, json
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from database import get_session
from api.models.models import Lodging

lodgings_bp = Blueprint('lodgings', url_prefix='/lodgings')

def parse_date(date_str):
    """Convert string to date object"""
    return datetime.strptime(date_str, '%Y-%m-%d').date()

@lodgings_bp.get("/")
async def get_lodgings(request):
    """Get all lodgings with pagination and filtering"""
    # Parse query parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    name = request.args.get('name')
    start_date = request.args.get('start_date')
    min_rooms = request.args.get('min_rooms')
    
    async with get_session() as session:
        # Build base query
        query = select(Lodging)
        count_query = select(func.count(Lodging.id))
        
        # Apply filters if provided
        if name:
            query = query.filter(Lodging.name.ilike(f"%{name}%"))
            count_query = count_query.filter(Lodging.name.ilike(f"%{name}%"))
        if start_date:
            date_obj = parse_date(start_date)
            query = query.filter(Lodging.date_start >= date_obj)
            count_query = count_query.filter(Lodging.date_start >= date_obj)
        if min_rooms:
            query = query.filter(Lodging.room_count >= int(min_rooms))
            count_query = count_query.filter(Lodging.room_count >= int(min_rooms))
        
        # Get total count
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Execute query
        result = await session.execute(query)
        lodgings = result.scalars().all()
        
        # Build response with HATEOAS links
        response = {
            "data": [lodging.to_dict() for lodging in lodgings],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            },
            "_links": {
                "self": f"/api/lodgings?page={page}&per_page={per_page}",
                "next": f"/api/lodgings?page={page+1}&per_page={per_page}" 
                       if page * per_page < total else None,
                "prev": f"/api/lodgings?page={page-1}&per_page={per_page}" 
                       if page > 1 else None
            }
        }
        return json(response)

@lodgings_bp.get("/<lodging_id:int>")
async def get_lodging(request, lodging_id):
    """Get a specific lodging"""
    async with get_session() as session:
        result = await session.execute(
            select(Lodging).filter(Lodging.id == lodging_id)
        )
        lodging = result.scalar_one_or_none()
        
        if not lodging:
            return json({"error": "Lodging not found"}, status=404)
        
        # Return with HATEOAS links
        response = {
            "data": lodging.to_dict(),
            "_links": {
                "self": f"/api/lodgings/{lodging_id}",
                "collection": "/api/lodgings",
                "update": {
                    "href": f"/api/lodgings/{lodging_id}",
                    "method": "PUT"
                },
                "delete": {
                    "href": f"/api/lodgings/{lodging_id}",
                    "method": "DELETE"
                }
            }
        }
        return json(response)

@lodgings_bp.post("/")
async def create_lodging(request):
    """Create a new lodging"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'date_start', 'date_end', 'room_count']
    if not all(field in data for field in required_fields):
        return json({
            "error": "Missing required fields",
            "required_fields": required_fields
        }, status=400)
    
    try:
        # Parse dates
        data['date_start'] = parse_date(data['date_start'])
        data['date_end'] = parse_date(data['date_end'])
        
        # Validate date range
        if data['date_start'] > data['date_end']:
            return json({
                "error": "Start date must be before end date"
            }, status=400)
        
        # Validate room count
        if int(data['room_count']) < 1:
            return json({
                "error": "Room count must be at least 1"
            }, status=400)
        
        async with get_session() as session:
            lodging = Lodging(**data)
            session.add(lodging)
            await session.commit()
            
            response = {
                "data": lodging.to_dict(),
                "_links": {
                    "self": f"/api/lodgings/{lodging.id}",
                    "collection": "/api/lodgings"
                }
            }
            # 201 Created for successful resource creation
            return json(response, status=201, headers={
                'Location': f"/api/lodgings/{lodging.id}"
            })
    except ValueError as e:
        return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@lodgings_bp.put("/<lodging_id:int>")
async def update_lodging(request, lodging_id):
    """Update an existing lodging"""
    data = request.json
    async with get_session() as session:
        result = await session.execute(
            select(Lodging).filter(Lodging.id == lodging_id)
        )
        lodging = result.scalar_one_or_none()
        
        if not lodging:
            return json({"error": "Lodging not found"}, status=404)
        
        try:
            # Parse dates if provided
            if 'date_start' in data:
                data['date_start'] = parse_date(data['date_start'])
            if 'date_end' in data:
                data['date_end'] = parse_date(data['date_end'])
            
            # Validate room count if provided
            if 'room_count' in data and int(data['room_count']) < 1:
                return json({
                    "error": "Room count must be at least 1"
                }, status=400)
            
            # Update fields
            for key, value in data.items():
                if hasattr(lodging, key):
                    setattr(lodging, key, value)
            
            # Validate date range
            if lodging.date_start > lodging.date_end:
                return json({
                    "error": "Start date must be before end date"
                }, status=400)
            
            await session.commit()
            return json({
                "data": lodging.to_dict(),
                "_links": {
                    "self": f"/api/lodgings/{lodging.id}",
                    "collection": "/api/lodgings"
                }
            })
        except ValueError as e:
            return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

@lodgings_bp.delete("/<lodging_id:int>")
async def delete_lodging(request, lodging_id):
    """Delete a lodging"""
    async with get_session() as session:
        result = await session.execute(
            select(Lodging).filter(Lodging.id == lodging_id)
        )
        lodging = result.scalar_one_or_none()
        
        if not lodging:
            return json({"error": "Lodging not found"}, status=404)
        
        await session.delete(lodging)
        await session.commit()
        # 204 No Content for successful deletion
        return json({}, status=204)