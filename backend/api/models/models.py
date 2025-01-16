# backend/api/models/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class TravelAgent(Base):
    __tablename__ = "travel_agents"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100), nullable=False, unique=True)
    agency = Column(String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "agency": self.agency
        }

class TravelAgency(Base):
    __tablename__ = "travel_agencies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    logo = Column(String(200))  # URL or path to logo

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "logo": self.logo
        }

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True)
    tour_name = Column(String(100), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tour_name": self.tour_name,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end)
        }

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    transporter = Column(String(100))
    mode = Column(String(50))
    location_start = Column(String(100), nullable=False)
    location_end = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
            "transporter": self.transporter,
            "mode": self.mode,
            "location_start": self.location_start,
            "location_end": self.location_end
        }

class Lodging(Base):
    __tablename__ = "lodgings"
    
    id = Column(Integer, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    address = Column(String(200))
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    room_count = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
            "address": self.address,
            "name": self.name,
            "phone": self.phone,
            "room_count": self.room_count
        }
