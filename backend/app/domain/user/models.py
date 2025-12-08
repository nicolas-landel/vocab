from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY
from datetime import datetime
from app.core.database import Base
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    native_language = Column(String, ForeignKey("languages.code"), nullable=True)
    learning_languages = Column(ARRAY(String), nullable=True)


