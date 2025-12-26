from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Enum, DateTime, Text, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class Difficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class WordType(str, enum.Enum):
    NOUN = "NOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    ADVERB = "ADVERB"
    OTHER = "OTHER"


class Language(Base):
    __tablename__ = "languages"
    __mapper_args__ = {
        'exclude_properties': ['id']
    }

    id = None
    
    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Domain(Base):
    __tablename__ = "domains"

    id = None
    
    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)


class MasterWord(Base):
    __tablename__ = "master_words"

    id = None
    
    concept = Column(String, primary_key=True, index=True)
    domain_code = Column(String, ForeignKey("domains.code"), nullable=False)
    domain = relationship("Domain", foreign_keys=[domain_code])
    difficulty = Column(Enum(Difficulty), default=Difficulty.EASY, nullable=False)
    image_url = Column(String, nullable=True)
    word_type = Column(Enum(WordType), nullable=True)

class Translation(Base):
    __tablename__ = "translations"
    
    master_word_concept = Column(String, ForeignKey("master_words.concept", ondelete="CASCADE"), nullable=False)
    master_word = relationship("MasterWord", foreign_keys=[master_word_concept], backref="translations")
    text = Column(String, nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    language = relationship("Language", foreign_keys=[language_code])
    audio_url = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    plural_text = Column(String, nullable=True)
    sentence_example = Column(Text, nullable=True)
    synonyms = Column(ARRAY(String), nullable=True)
    
    __table_args__ = (
        UniqueConstraint('master_word_concept', 'language_code', name='unique_translation'),
    )


class UserTranslation(Base):
    """Tracks user-specific data for translations (e.g., words they've marked as 'already known')"""
    __tablename__ = "user_translations"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    translation_id = Column(UUID(as_uuid=True), ForeignKey("translations.id", ondelete="CASCADE"), nullable=False)
    is_known = Column(Boolean, default=False)  # User marked as "already know this word"
    
    # Note: User relationship will be configured when User model is imported
    # user = relationship("User")
    translation = relationship("Translation")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'translation_id', name='unique_user_translation'),
    )


