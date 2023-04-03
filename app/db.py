from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine('postgresql://postgres:password@postgres:5432/ocr-api',echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)