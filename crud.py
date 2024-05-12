from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate
from cachetools import TTLCache

# Initialize a cache with a time-to-live (TTL) of 60 seconds
cache = TTLCache(maxsize=1000, ttl=60)

def create_user(db: Session, user_data: UserCreate):
    user = User(name=user_data.name)
    db.add(user)
    db.commit()
    cache[user.id] = user
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    if user_id in cache:
        print("cache")
        return cache[user_id]
    else:
        # Query database to get user
        user = db.query(User).filter(User.id == user_id).first()
        # Cache the user
        if(user):
            cache[user_id] = user
        return user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = user_data.name
        db.commit()
        cache[user_id] = user
        db.refresh(user)
        
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user) 
        db.commit()
        return True
    return False

def search_users(db: Session, name: str):
    return db.query(User).filter(User.name.ilike(f'%{name}%')).all()
