from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .models import Difficulty


class LanguageBase(BaseModel):
    code: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class LanguageCreate(LanguageBase):
    pass

class LanguageSchema(LanguageBase):
    pass

class WordBase(BaseModel):
    text: str
    language_code: str
    domain: str
    difficulty: Difficulty

class WordCreate(WordBase):
    pass

class WordSchema(WordBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TranslationBase(BaseModel):
    source_word_id: int
    target_word_id: int

class TranslationCreate(TranslationBase):
    pass
