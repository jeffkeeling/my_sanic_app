# backend/api/routes/trips.py
from sanic import Blueprint, json
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from database import get_session
from api.models.models import Trip

trips_bp = Blueprint('trips', url_prefix='/trips')

def parse_date(date_str):
    """Convert string to date object"""
    return datetime.strptime(date_str, '%Y-%m-%d').date()

@trips_bp.get("/")
async def get_trips(request):
    """Get all trips with pagination and filtering"""
    # Parse query parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    mode = request.args.get('mode')
    transporter = request.args.get('transporter')
    start_date = request.args.get('start_date')
    location = request.args.get('location')  # Search in both start and end locations
    
    async with get_session() as session:
        # Build base query
        query = select(Trip)
        count_query = select(func.count(Trip.id))
        
        # Apply filters if provided
        if mode:
            query = query.filter(Trip.mode == mode)
            count_query = count_query.filter(Trip.mode == mode)
        if transporter:
            query = query.filter(Trip.transporter.ilike(f"%{transporter}%"))
            count_query = count_query.filter(Trip.transporter.ilike(f"%{transporter}%"))
        if start_date:
            date_obj = parse_date(start_date)
            query = query.filter(Trip.date_start >= date_obj)
            count_query = count_query.filter(Trip.date_start >= date_obj)
        if location:
            # Search in both start and end locations
            query = query.filter(
                (Trip.location_start.ilike(f"%{location}%")) |
                (Trip.location_end.ilike(f"%{location}%"))
            )
            count_query = count_query.filter(
                (Trip.location_start.ilike(f"%{location}%")) |
                (Trip.location_end.ilike(f"%{location}%"))
            )
        
        # Get total count
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Execute query
        result = await session.execute(query)
        trips = result.scalars().all()
        
        # Build response with HATEOAS links
        response = {
            "data": [trip.to_dict() for trip in trips],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            },
            "_links": {
                "self": f"/api/trips?page={page}&per_page={per_page}",
                "next": f"/api/trips?page={page+1}&per_page={per_page}" 
                       if page * per_page < total else None,
                "prev": f"/api/trips?page={page-1}&per_page={per_page}" 
                       if page > 1 else None
            }
        }
        return json(response)

@trips_bp.get("/<trip_id:int>")
async def get_trip(request, trip_id):
    """Get a specific trip"""
    async with get_session() as session:
        result = await session.execute(
            select(Trip).filter(Trip.id == trip_id)
        )
        trip = result.scalar_one_or_none()
        
        if not trip:
            return json({"error": "Trip not found"}, status=404)
        
        # Return with HATEOAS links
        response = {
            "data": trip.to_dict(),
            "_links": {
                "self": f"/api/trips/{trip_id}",
                "collection": "/api/trips",
                "update": {
                    "href": f"/api/trips/{trip_id}",
                    "method": "PUT"
                },
                "delete": {
                    "href": f"/api/trips/{trip_id}",
                    "method": "DELETE"
                }
            }
        }
        return json(response)

@trips_bp.post("/")
async def create_trip(request):
    """Create a new trip"""
    data = request.json
    
    # Validate required fields
    required_fields = ['date_start', 'date_end', 'location_start', 'location_end']
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
        
        # Validate mode if provided
        if 'mode' in data and data['mode'] not in ['flight', 'train', 'bus', 'car', 'ship']:
            return json({
                "error": "Invalid mode of transport. Must be one of: flight, train, bus, car, ship"
            }, status=400)
        
        async with get_session() as session:
            trip = Trip(**data)
            session.add(trip)
            await session.commit()
            
            response = {
                "data": trip.to_dict(),
                "_links": {
                    "self": f"/api/trips/{trip.id}",
                    "collection": "/api/trips"
                }
            }
            # 201 Created for successful resource creation
            return json(response, status=201, headers={
                'Location': f"/api/trips/{trip.id}"
            })
    except ValueError as e:
        return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@trips_bp.put("/<trip_id:int>")
async def update_trip(request, trip_id):
    """Update an existing trip"""
    data = request.json
    async with get_session() as session:
        result = await session.execute(
            select(Trip).filter(Trip.id == trip_id)
        )
        trip = result.scalar_one_or_none()
        
        if not trip:
            return json({"error": "Trip not found"}, status=404)
        
        try:
            # Parse dates if provided
            if 'date_start' in data:
                data['date_start'] = parse_date(data['date_start'])
            if 'date_end' in data:
                data['date_end'] = parse_date(data['date_end'])
            
            # Validate mode if provided
            if 'mode' in data and data['mode'] not in ['flight', 'train', 'bus', 'car', 'ship']:
                return json({
                    "error": "Invalid mode of transport. Must be one of: flight, train, bus, car, ship"
                }, status=400)
            
            # Update fields
            for key, value in data.items():
                if hasattr(trip, key):
                    setattr(trip, key, value)
            
            # Validate date range
            if trip.date_start > trip.date_end:
                return json({
                    "error": "Start date must be before end date"
                }, status=400)
            
            await session.commit()
            return json({
                "data": trip.to_dict(),
                "_links": {
                    "self": f"/api/trips/{trip.id}",
                    "collection": "/api/trips"
                }
            })
        except ValueError as e:
            return json({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

@trips_bp.delete("/<trip_id:int>")
async def delete_trip(request, trip_id):
    """Delete a trip"""
    async with get_session() as session:
        result = await session.execute(
            select(Trip).filter(Trip.id == trip_id)
        )
        trip = result.scalar_one_or_none()
        
        if not trip:
            return json({"error": "Trip not found"}, status=404)
        
        await session.delete(trip)
        await session.commit()
        # 204 No Content for successful deletion
        return json({}, status=204)