from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import random
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="sport_connect_app")

from . import models
from .database import engine, get_db
from .ai_agent import process_chat

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Local Sports Tournament Discovery API")

# --- Pydantic Schemas ---
class TournamentBase(BaseModel):
    title: str
    sport: str
    location: str
    entry_fee: float
    prize_pool: str
    organizer_name: str
    contact_details: str
    tournament_date: str
    description: str
    is_verified: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str = "user"

class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    id: int

    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    tournament_id: int
    player_name: str
    player_email: str
    team_name: Optional[str] = None

class RegistrationOut(RegistrationCreate):
    id: int

    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    email: str
    sport: str
    location: str

class ChatRequest(BaseModel):
    message: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to Local Sports Tournament Discovery API"}

@app.post("/tournaments/", response_model=Tournament)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    db_tournament = models.Tournament(**tournament.model_dump())
    
    if db_tournament.location and (db_tournament.latitude is None or db_tournament.longitude is None):
        try:
            loc = geolocator.geocode(db_tournament.location, timeout=5)
            if loc:
                db_tournament.latitude = loc.latitude
                db_tournament.longitude = loc.longitude
        except Exception as e:
            print(f"Geocoding failed for {db_tournament.location}: {e}")
            
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    
    # Simulate sending notifications
    subs = db.query(models.NotificationSubscription).filter(
        models.NotificationSubscription.sport.ilike(f"%{tournament.sport}%"),
        models.NotificationSubscription.location.ilike(f"%{tournament.location}%")
    ).all()
    
    if subs:
        print(f"--- NOTIFICATION SENT TO {len(subs)} SUBSCRIBERS for new {tournament.sport} tournament in {tournament.location} ---")
        
    return db_tournament

@app.get("/tournaments/", response_model=List[Tournament])
def read_tournaments(sport: Optional[str] = None, location: Optional[str] = None, source: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Tournament)
    if sport:
        query = query.filter(models.Tournament.sport.ilike(f"%{sport}%"))
    if location:
        query = query.filter(models.Tournament.location.ilike(f"%{location}%"))
    if source:
        query = query.filter(models.Tournament.source == source)
    return query.all()

@app.post("/tournaments/mock-government")
def mock_government_data(db: Session = Depends(get_db)):
    count = 0
    sports = ["Cricket", "Hockey", "Football", "Badminton", "Athletics"]
    locations = ["New Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]
    for i in range(3):
        sport = random.choice(sports)
        loc = random.choice(locations)
        title = f"National {sport} Championship 2026"
        exists = db.query(models.Tournament).filter(
            models.Tournament.title == title,
            models.Tournament.source == "government"
        ).first()
        if not exists:
            lat, lng = None, None
            try:
                geo = geolocator.geocode(loc, timeout=5)
                if geo:
                    lat, lng = geo.latitude, geo.longitude
            except:
                pass
            db_tourney = models.Tournament(
                title=title, sport=sport, location=loc, entry_fee=0.0,
                prize_pool="Govt Sponsored + Medal", organizer_name="Ministry of Sports",
                contact_details="myas@gov.in", tournament_date="2026-05-15",
                description="Official Government Sponsored Tournament. Highly verified platform.",
                is_verified=True, source="government", latitude=lat, longitude=lng
            )
            db.add(db_tourney)
            count += 1
    if count > 0:
        db.commit()
        return {"message": f"Added {count} official government tournaments."}
    return {"message": "Government data up to date."}

@app.post("/register/")
def register_for_tournament(registration: RegistrationCreate, db: Session = Depends(get_db)):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == registration.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    db_registration = models.Registration(**registration.model_dump())
    db.add(db_registration)
    db.commit()
    return {"message": "Successfully registered!"}

@app.get("/tournaments/{tournament_id}/registrations", response_model=List[RegistrationOut])
def get_tournament_registrations(tournament_id: int, db: Session = Depends(get_db)):
    registrations = db.query(models.Registration).filter(models.Registration.tournament_id == tournament_id).all()
    return registrations

@app.post("/subscribe/")
def subscribe_notifications(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    db_sub = models.NotificationSubscription(**sub.model_dump())
    db.add(db_sub)
    db.commit()
    return {"message": "Successfully subscribed to notifications!"}

@app.post("/ai/chat")
def ai_chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Fetch all tournaments to provide context to the AI
    tournaments = db.query(models.Tournament).all()
    # Call the AI agent
    response_text = process_chat(request.message, tournaments)
    return {"response": response_text}
