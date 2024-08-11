import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    key = Column(String, index=True)


class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    is_valid = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)
