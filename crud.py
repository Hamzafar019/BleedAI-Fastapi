from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate
from cachetools import TTLCache

# Initialize a cache with a time-to-live (TTL) of 60 seconds
cache = TTLCache(maxsize=1000, ttl=60)

def create_user(db: Session, user_data: UserCreate):
    db_user = User(name=user_data.name)
    db.add(db_user)
    db.commit()
    cache[db_user.id] = db_user
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    if user_id in cache:
        print("tatt")
        return cache[user_id]
    else:
        # Query database to get user
        user = db.query(User).filter(User.id == user_id).first()
        # Cache the user
        if(user):
            cache[user_id] = user
        return user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user_data.name
        db.commit()
        cache[db_user.id] = db_user
        db.refresh(db_user)
        
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        del cache[db_user.id]
        return True
    return False

def search_users(db: Session, name: str):
    return db.query(User).filter(User.name.ilike(f'%{name}%')).all()
