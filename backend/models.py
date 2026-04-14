from sqlalchemy import Column, Integer, String, Date, Float, Text, Boolean
from .database import Base

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    sport = Column(String, index=True)
    location = Column(String, index=True)
    entry_fee = Column(Float)
    prize_pool = Column(String)
    organizer_name = Column(String)
    contact_details = Column(String)
    tournament_date = Column(String)
    description = Column(Text)
    is_verified = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    source = Column(String, default="user")

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, index=True)
    player_name = Column(String)
    player_email = Column(String)
    team_name = Column(String, nullable=True)

class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    sport = Column(String, index=True)
    location = Column(String, index=True)
