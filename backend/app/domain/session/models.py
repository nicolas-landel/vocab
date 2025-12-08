from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class SessionType(str, enum.Enum):
    COMPREHENSION = "COMPREHENSION"
    EXPRESSION = "EXPRESSION"
    MIXED = "MIXED"


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_lang_code = Column(String, ForeignKey("languages.code"), nullable=False)
    target_lang_code = Column(String, ForeignKey("languages.code"), nullable=False)
    domain = Column(String, nullable=True) # If null, all domains
    difficulty = Column(String, nullable=True) # If null, mixed difficulty
    session_type = Column(Enum(SessionType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, nullable=True) # Percentage or count
    
    user = relationship("app.domain.user.models.User")
    results = relationship("SessionResult", back_populates="session")

class SessionResult(Base):
    __tablename__ = "session_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    
    session = relationship("Session", back_populates="results")
    word = relationship("app.domain.vocab.models.Word")


class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey(".id"), nullable=False, index=True)
    translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False, index=True)
    
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    last_reviewed = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("app.domain.user.models.User") 
    word = relationship("Word")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'word_id', name='unique_user_word_progress'),
    )
