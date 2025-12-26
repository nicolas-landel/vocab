from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
from datetime import datetime
from app.core.database import Base
from sqlalchemy import ForeignKey


class LanguageLevelEnum(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    NATIVE = "NATIVE"


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    is_active = Column(Boolean, default=True)
    native_language = Column(String, ForeignKey("languages.code"), nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # 'google', 'github', etc.
    oauth_id = Column(String, nullable=True)  # Provider's user ID
    full_name = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)


class UserLanguage(Base):
    __tablename__ = "user_languages"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    level = Column(Enum(LanguageLevelEnum), nullable=False)
    is_learning = Column(Boolean, default=True)
    