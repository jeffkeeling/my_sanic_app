# backend/api/routes/itineraries.py
from sanic import Blueprint, json
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from database import get_session
from api.models.models import Itinerary

itineraries_bp = Blueprint('itineraries', url_prefix='/itineraries')

def parse_date(date_str):
    """Convert string to date object"""
    return datetime.strptime(date_str, '%Y-%m-%d').date()

@itineraries_bp.get("/")
async def get_itineraries(request):
    """Get all itineraries with pagination and filtering"""
    # Parse query parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    tour_name = request.args.get('tour_name')
    start_date = request.args.get('start_date')
    
    async with get_session() as session:
        # Build base query
        query = select(Itinerary)
        count_query = select(func.count(Itinerary.id))
        
        # Apply filters if provided
        if tour_name:
            query = query.filter(Itinerary.tour_name.ilike(f"%{tour_name}%"))
            count_query = count_query.filter(Itinerary.tour_name.ilike(f"%{tour_name}%"))
        if start_date:
            date_obj = parse_date(start_date)
            query = query.filter(Itinerary.date_start >= date_obj)
            count_query = count_query.filter(Itinerary.date_start >= date_obj)
        
        # Get total count
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Execute query
        result = await session.execute(query)
        itineraries = result.scalars().all()
        
        # Build response with HATEOAS links
        response = {
            "data": [itinerary.to_dict() for itinerary in itineraries],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            },
            "_links": {
                "self": f"/api/itineraries?page={page}&per_page={per_page}",
                "next": f"/api/itineraries?page={page+1}&per_page={per_page}" 
                       if page * per_page < total else None,
                "prev": f"/api/itineraries?page={page-1}&per_page={per_page}" 
                       if page > 1 else None
            }
        }
        return json(response)

@itineraries_bp.get("/<itinerary_id:int>")
async def get_itinerary(request, itinerary_id):
    """Get a specific itinerary"""
    async with get_session() as session:
        result = await session.execute(
            select(Itinerary).filter(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            return json({"error": "Itinerary not found"}, status=404)
        
        # Return with HATEOAS links
        response = {
            "data": itinerary.to_dict(),
            "_links": {
                "self": f"/api/itineraries/{itinerary_id}",
                "collection": "/api/itineraries",
                "trips": f"/api/trips?itinerary_id={itinerary_id}",
                "lodgings": f"/api/lodgings?itinerary_id={itinerary_id}",
                "update": {
                    "href": f"/api/itineraries/{itinerary_id}",
                    "method": "PUT"
                },
                "delete": {
                    "href": f"/api/itineraries/{itinerary_id}",
                    "method": "DELETE"
                }
            }
        }
        return json(response)

@itineraries_bp.post("/")
async def create_itinerary(request):
    """Create a new itinerary"""
    data = request.json
    
    # Validate required fields
    required_fields = ['tour_name', 'date_start', 'date_end']
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
        
        async with get_session() as session:
            itinerary = Itinerary(**data)
            session.add(itinerary)
            await session.commit()
            
            response = {
                "data": itinerary.to_dict(),
                "_links": {
                    "self": f"/api/itineraries/{itinerary.id}",
                    "collection": "/api/itineraries"
                }
            }
            # 201 Created for successful resource creation
            return json(response, status=201, headers={
                'Location': f"/api/itineraries/{itinerary.id}"
            })
    except ValueError as e:
        return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@itineraries_bp.put("/<itinerary_id:int>")
async def update_itinerary(request, itinerary_id):
    """Update an existing itinerary"""
    data = request.json
    async with get_session() as session:
        result = await session.execute(
            select(Itinerary).filter(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            return json({"error": "Itinerary not found"}, status=404)
        
        try:
            # Parse dates if provided
            if 'date_start' in data:
                data['date_start'] = parse_date(data['date_start'])
            if 'date_end' in data:
                data['date_end'] = parse_date(data['date_end'])
            
            # Update fields
            for key, value in data.items():
                if hasattr(itinerary, key):
                    setattr(itinerary, key, value)
            
            # Validate date range
            if itinerary.date_start > itinerary.date_end:
                return json({
                    "error": "Start date must be before end date"
                }, status=400)
            
            await session.commit()
            return json({
                "data": itinerary.to_dict(),
                "_links": {
                    "self": f"/api/itineraries/{itinerary.id}",
                    "collection": "/api/itineraries"
                }
            })
        except ValueError as e:
            return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

@itineraries_bp.delete("/<itinerary_id:int>")
async def delete_itinerary(request, itinerary_id):
    """Delete an itinerary"""
    async with get_session() as session:
        result = await session.execute(
            select(Itinerary).filter(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        
        if not itinerary:
            return json({"error": "Itinerary not found"}, status=404)
        
        await session.delete(itinerary)
        await session.commit()
        # 204 No Content for successful deletion
        return json({}, status=204)