import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import database

load_dotenv()

# Create the SQLAlchemy engine
if database.DATABASE_TYPE == "postgres":
    engine = create_engine(database.DATABASE_URL, echo=True)
elif database.DATABASE_TYPE == "mongodb":
    # Implement MongoDB engine setup here
    # You'll likely need to use pymongo for MongoDB
    # See pymongo documentation for details
    pass
else:
    raise ValueError("Invalid database type specified in .env file.")

# Create the base class for all models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the database models here
# ...
# Example models (replace with your actual models):

# User model (if storing user data)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    discriminator = Column(String, nullable=False)
    # ... (add other attributes as needed)

# Server model (if storing server data)
class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # ... (add other attributes as needed)

# Playlist model
class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    songs = Column(ARRAY(String), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    server = relationship("Server", backref="playlists")
    owner = relationship("User", backref="playlists")

# ... (add other models as needed)