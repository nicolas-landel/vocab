from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY
from datetime import datetime
from app.core.database import Base
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    is_active = Column(Boolean, default=True)
    native_language = Column(String, ForeignKey("languages.code"), nullable=True)
    learning_languages = Column(ARRAY(String), nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # 'google', 'github', etc.
    oauth_id = Column(String, nullable=True)  # Provider's user ID
    full_name = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)


