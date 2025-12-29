from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class SessionType(str, enum.Enum):
    COMPREHENSION = "COMPREHENSION"
    EXPRESSION = "EXPRESSION"
    MIXED = "MIXED"


class SessionConfig(Base):
    """Configuration for each session - created before starting a session"""
    __tablename__ = "session_configs"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    native_language = Column(String, ForeignKey("languages.code"), nullable=False)
    language_tested = Column(String, ForeignKey("languages.code"), nullable=False)
    difficulty = Column(String, nullable=True)  # Can be null for mixed
    domain = Column(String, nullable=True)  # Can be null for all domains
    session_type = Column(Enum(SessionType), nullable=False)
    
    user = relationship("User", foreign_keys=[user_id])
    native_lang = relationship("Language", foreign_keys=[native_language])
    tested_lang = relationship("Language", foreign_keys=[language_tested])
    session = relationship("Session", back_populates="config", uselist=False)


class Session(Base):
    __tablename__ = "sessions"
    
    config_id = Column(UUID(as_uuid=True), ForeignKey("session_configs.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    source_lang_code = Column(String, ForeignKey("languages.code"), nullable=False)
    target_lang_code = Column(String, ForeignKey("languages.code"), nullable=False)
    domain = Column(String, nullable=True)  # If null, all domains
    difficulty = Column(String, nullable=True)  # If null, mixed difficulty
    session_type = Column(Enum(SessionType), nullable=False)
    score = Column(Integer, nullable=True)  # Percentage or count
    completed_at = Column(DateTime, nullable=True)  # When session was finished
    
    config = relationship("SessionConfig", back_populates="session")
    user = relationship("User", foreign_keys=[user_id])
    source_language = relationship("Language", foreign_keys=[source_lang_code])
    target_language = relationship("Language", foreign_keys=[target_lang_code])
    results = relationship("SessionWord", back_populates="session", cascade="all, delete-orphan")


class SessionWord(Base):
    """Stores individual word results for each session"""
    __tablename__ = "session_results"
    
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    translation_from_id = Column(UUID(as_uuid=True), ForeignKey("translations.id", ondelete="CASCADE"), nullable=False)
    translation_to_id = Column(UUID(as_uuid=True), ForeignKey("translations.id", ondelete="CASCADE"), nullable=False)
    from_language = Column(String, ForeignKey("languages.code"), nullable=False)
    to_language = Column(String, ForeignKey("languages.code"), nullable=False)
    correct = Column(Boolean, nullable=True, default=None)
    user_answer = Column(String, nullable=True)
    
    session = relationship("Session", back_populates="results")
    translation_from = relationship("Translation", foreign_keys=[translation_from_id])
    translation_to = relationship("Translation", foreign_keys=[translation_to_id])


class UserProgress(Base):
    """Tracks overall user progress for each translation"""
    __tablename__ = "user_progress"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    translation_id = Column(UUID(as_uuid=True), ForeignKey("translations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    last_reviewed = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    translation = relationship("Translation")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'translation_id', name='unique_user_translation_progress'),
    )
