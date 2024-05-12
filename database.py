from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Configure database connection
hostname: str = "localhost"
username: str = "root"
password: str = "emotisement"
port: int = 3306
database: str = "user"

engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
