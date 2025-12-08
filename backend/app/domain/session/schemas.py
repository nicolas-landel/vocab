from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .models import SessionType
from app.domain.vocab.schemas import WordSchema


class SessionCreate(BaseModel):
    source_lang_code: str
    target_lang_code: str
    domain: Optional[str] = None
    difficulty: Optional[str] = None
    session_type: SessionType


class SessionResultCreate(BaseModel):
    word_id: int
    correct: bool


class SessionResultSchema(SessionResultCreate):
    id: int
    session_id: int
    word: WordSchema
    model_config = ConfigDict(from_attributes=True)


class SessionSchema(SessionCreate):
    id: int
    user_id: int
    created_at: datetime
    score: Optional[int] = None
    results: List[SessionResultSchema] = []
    
    model_config = ConfigDict(from_attributes=True)