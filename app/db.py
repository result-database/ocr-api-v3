from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine('postgresql://admin:admin-pass@postgres:5432/ocr-api',echo=False)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)