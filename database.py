from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class ParsedData(Base):
    __tablename__ = "parsed_data"
    
    id = Column(Integer, primary_key=True, index=True)  # Database-generated ID
    name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    user_id = Column(String, unique=True, nullable=False)  # User ID with alias
    bio = Column(Text, nullable=False)
    version = Column(Float, nullable=False)

# Create tables
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get and close the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
