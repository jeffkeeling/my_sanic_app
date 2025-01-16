# backend/api/routes/users.py
from sanic import Blueprint, json
from sqlalchemy.future import select
from database import get_session
from api.models.user import User
import logging

logger = logging.getLogger(__name__)

# Create a Blueprint for user routes
users_bp = Blueprint('users', url_prefix='/users')

@users_bp.get("/")
async def get_users(request):
    async with get_session() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return json([{
                "id": user.id,
                "name": user.name,
                "email": user.email
            } for user in users])
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return json({"error": "Failed to fetch users"}, status=500)

@users_bp.post("/")
async def create_user(request): # Function is marked as async
    # The function is marked async because it contains operations that might take time (database operations)
    # These operations are synchronous (happen immediately):
    user_data = request.json
    if not user_data or 'name' not in user_data or 'email' not in user_data:
        return json({"error": "Name and email are required"}, status=400)
    
    # This starts an async context manager
    async with get_session() as session:
        try:
            # These are synchronous operations:
            new_user = User(
                name=user_data["name"],
                email=user_data["email"]
            )
            session.add(new_user)

            # This is async - might take time to write to database
            await session.commit()
            
            # This is synchronous - happens immediately
            return json({
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }, status=201)
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating user: {e}")
            return json({"error": "Failed to create user"}, status=500)

@users_bp.delete("/<user_id:int>")
async def delete_user(request, user_id):
    async with get_session() as session:
        try:
            result = await session.execute(
                select(User).filter(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if user is None:
                return json({"error": "User not found"}, status=404)
                
            await session.delete(user)
            await session.commit()
            return json({"message": "User deleted successfully"})
        except Exception as e:
            await session.rollback()
            logger.error(f"Error deleting user: {e}")
            return json({"error": "Failed to delete user"}, status=500)