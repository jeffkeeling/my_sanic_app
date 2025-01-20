# backend/seed.py
import asyncio
from datetime import date, timedelta
from database import init_db, get_session
from api.models.models import TravelAgency, Itinerary, Trip, Lodging, User

async def seed_database():
    # Initialize database (creates tables)
    await init_db()
    
    async with get_session() as session:
        try:
            # Create travel agencies
            agencies = [
                TravelAgency(
                    name="Worldwide Adventures",
                    phone="555-0100",
                    address="123 Travel Lane",
                    logo="worldwide_adventures.png"
                ),
                TravelAgency(
                    name="Luxury Travels",
                    phone="555-0200",
                    address="456 First Class Blvd",
                    logo="luxury_travels.png"
                )
            ]
            
            # Add agencies to session
            for agency in agencies:
                session.add(agency)
            
            # Flush to get agency IDs
            await session.flush()
            
            # Create users with agency assignments
            users = [
                User(
                    name="John Doe",
                    email="john@example.com",
                    travel_agency_id=agencies[0].id
                ),
                User(
                    name="Jane Smith",
                    email="jane@example.com",
                    travel_agency_id=agencies[0].id
                ),
                User(
                    name="Bob Johnson",
                    email="bob@example.com",
                    travel_agency_id=agencies[1].id
                )
            ]
            
            # Add users to session
            for user in users:
                session.add(user)
            
            # Flush to get user IDs
            await session.flush()
            
            # Create itineraries for users
            start_date = date(2024, 6, 1)
            itineraries = [
                # John's Europe Tour
                Itinerary(
                    tour_name="Europe Adventure",
                    date_start=start_date,
                    date_end=start_date + timedelta(days=14),
                    user_id=users[0].id
                ),
                # Jane's Asia Tour
                Itinerary(
                    tour_name="Asian Discovery",
                    date_start=start_date + timedelta(days=30),
                    date_end=start_date + timedelta(days=45),
                    user_id=users[1].id
                ),
                # Bob's Luxury Mediterranean
                Itinerary(
                    tour_name="Mediterranean Luxury",
                    date_start=start_date + timedelta(days=60),
                    date_end=start_date + timedelta(days=75),
                    user_id=users[2].id
                )
            ]
            
            # Add itineraries to session
            for itinerary in itineraries:
                session.add(itinerary)
            
            # Flush to get itinerary IDs
            await session.flush()
            
            # Create trips for each itinerary
            trips = [
                # John's Europe trips
                Trip(
                    date_start=start_date,
                    date_end=start_date + timedelta(days=1),
                    transporter="Eurostar",
                    mode="train",
                    location_start="London",
                    location_end="Paris",
                    itinerary_id=itineraries[0].id
                ),
                Trip(
                    date_start=start_date + timedelta(days=5),
                    date_end=start_date + timedelta(days=5),
                    transporter="Air France",
                    mode="flight",
                    location_start="Paris",
                    location_end="Rome",
                    itinerary_id=itineraries[0].id
                ),
                # Jane's Asia trips
                Trip(
                    date_start=start_date + timedelta(days=30),
                    date_end=start_date + timedelta(days=31),
                    transporter="Japan Airlines",
                    mode="flight",
                    location_start="Tokyo",
                    location_end="Seoul",
                    itinerary_id=itineraries[1].id
                )
            ]
            
            # Add trips to session
            for trip in trips:
                session.add(trip)
            
            # Create lodgings for each itinerary
            lodgings = [
                # John's Europe lodgings
                Lodging(
                    date_start=start_date + timedelta(days=1),
                    date_end=start_date + timedelta(days=5),
                    name="Paris Hilton",
                    address="123 Champs-Élysées",
                    phone="33-1-234567",
                    room_count=1,
                    itinerary_id=itineraries[0].id
                ),
                Lodging(
                    date_start=start_date + timedelta(days=5),
                    date_end=start_date + timedelta(days=10),
                    name="Rome Luxury Hotel",
                    address="45 Vatican Road",
                    phone="39-06-123456",
                    room_count=1,
                    itinerary_id=itineraries[0].id
                ),
                # Jane's Asia lodgings
                Lodging(
                    date_start=start_date + timedelta(days=31),
                    date_end=start_date + timedelta(days=36),
                    name="Seoul Grand Hotel",
                    address="789 Gangnam Blvd",
                    phone="82-2-345678",
                    room_count=2,
                    itinerary_id=itineraries[1].id
                )
            ]
            
            # Add lodgings to session
            for lodging in lodgings:
                session.add(lodging)
            
            # Commit all changes
            await session.commit()
            print("Database seeded successfully!")
            
        except Exception as e:
            print(f"Error seeding database: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_database())