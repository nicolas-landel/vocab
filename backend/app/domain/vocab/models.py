from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Enum, DateTime
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
    PRONOUN = "PRONOUN"
    CONJUNCTION = "CONJUNCTION"
    PREPOSITION = "PREPOSITION"
    INTERJECTION = "INTERJECTION"
    OTHER = "OTHER"


class Language(Base):
    __tablename__ = "languages"
    
    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class MasterWord(Base):
    __tablename__ = "master_words"
    
    id = Column(Integer, primary_key=True, index=True)
    concept = Column(String, nullable=False, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=False)
    domain = relationship("Domain", foreign_keys=[domain_id])
    difficulty = Column(Enum(Difficulty), default=Difficulty.EASY, nullable=False)
    image_url = Column(String, nullable=True)
    word_type = Column(Enum(WordType), nullable=True)
    

class Translation(Base):
    __tablename__ = "translations"
    
    id = Column(Integer, primary_key=True, index=True)  
    master_word_id = Column(Integer, ForeignKey("master_words.id"), nullable=False)
    master_word = relationship("MasterWord", foreign_keys=[master_word_id])
    text = Column(String, nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    language = relationship("Language", foreign_keys=[language_code])
    audio_url = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    plurial_text = Column(String, nullable=True)
    sentence_example = Column(String, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('master_word_id', name='unique_translation'),
    )


