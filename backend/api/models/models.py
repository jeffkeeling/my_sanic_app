# backend/api/models/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    travel_agency_id = Column(Integer, ForeignKey('travel_agencies.id'), nullable=False)

    # Relationships
    travel_agency = relationship("TravelAgency", back_populates="users")
    itineraries = relationship("Itinerary", back_populates="user")

    def to_dict(self, include_itineraries=False):
        """
        Convert user to dictionary, optionally including itineraries
        """
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "travel_agency_id": self.travel_agency_id
        }
        
        # Only include itineraries if explicitly requested and loaded
        if include_itineraries and 'itineraries' in self.__dict__:
            data["itineraries"] = [itinerary.to_dict() for itinerary in self.itineraries]
        
        return data


class TravelAgency(Base):
    __tablename__ = "travel_agencies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    logo = Column(String(200))  # URL or path to logo

    # Add the relationship
    users = relationship(
        "User",
        back_populates="travel_agency",
        cascade="all, delete-orphan"
    )


    def to_dict(self, include_users=False):
        data = {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "logo": self.logo
        }
        
        if include_users:
            data["users"] = [user.to_dict() for user in self.users]
            
        return data

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True)
    tour_name = Column(String(100), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Add relationships to trips and lodgings
    trips = relationship("Trip", back_populates="itinerary", cascade="all, delete-orphan")
    lodgings = relationship("Lodging", back_populates="itinerary", cascade="all, delete-orphan")
    
    # Existing user relationship
    user = relationship("User", back_populates="itineraries")

    def to_dict(self, include_relationships=False):
        data = {
            "id": self.id,
            "tour_name": self.tour_name,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
            "user_id": self.user_id,
        }

        if include_relationships and 'trips' in self.__dict__:
            data["trips"] = [trip.to_dict() for trip in self.trips]
        if include_relationships and 'lodgings' in self.__dict__:
            data["lodgings"] = [lodging.to_dict() for lodging in self.lodgings]
            
        return data

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    transporter = Column(String(100))
    mode = Column(String(50))
    location_start = Column(String(100), nullable=False)
    location_end = Column(String(100), nullable=False)
    
    # Add foreign key to itinerary
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'), nullable=False)
    
    # Add relationship to itinerary
    itinerary = relationship("Itinerary", back_populates="trips")

    def to_dict(self):
        return {
            "id": self.id,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
            "transporter": self.transporter,
            "mode": self.mode,
            "location_start": self.location_start,
            "location_end": self.location_end,
            "itinerary_id": self.itinerary_id
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
    
    # Add foreign key to itinerary
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'), nullable=False)
    
    # Add relationship to itinerary
    itinerary = relationship("Itinerary", back_populates="lodgings")

    def to_dict(self):
        return {
            "id": self.id,
            "date_start": str(self.date_start),
            "date_end": str(self.date_end),
            "address": self.address,
            "name": self.name,
            "phone": self.phone,
            "room_count": self.room_count,
            "itinerary_id": self.itinerary_id
        }
