from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .models import Difficulty, WordType


# Language Schemas
class LanguageBase(BaseModel):
    code: str
    name: str

class LanguageCreate(LanguageBase):
    pass

class LanguageSchema(LanguageBase):
    model_config = ConfigDict(from_attributes=True)


# Domain Schemas
class DomainBase(BaseModel):
    code: str
    name: str

class DomainCreate(DomainBase):
    pass

class DomainSchema(DomainBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Translation Schemas
class TranslationBase(BaseModel):
    text: str
    language_code: str
    audio_url: Optional[str] = None
    gender: Optional[str] = None
    plural_text: Optional[str] = None
    sentence_example: Optional[str] = None
    synonyms: Optional[List[str]] = None

class TranslationCreate(TranslationBase):
    master_word_id: int

class TranslationSchema(TranslationBase):
    id: int
    master_word_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TranslationDetail(TranslationSchema):
    """Extended translation with language info"""
    language: LanguageSchema
    model_config = ConfigDict(from_attributes=True)


# MasterWord Schemas
class MasterWordBase(BaseModel):
    concept: str
    domain_id: int
    difficulty: Difficulty
    word_type: Optional[WordType] = None
    image_url: Optional[str] = None

class MasterWordCreate(MasterWordBase):
    translations: List[TranslationCreate] = []

class MasterWordSchema(MasterWordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MasterWordDetail(MasterWordSchema):
    """Extended master word with all translations"""
    translations: List[TranslationDetail] = []
    domain: DomainSchema
    model_config = ConfigDict(from_attributes=True)


# UserTranslation Schemas
class UserTranslationBase(BaseModel):
    translation_id: int
    is_known: bool = False

class UserTranslationCreate(UserTranslationBase):
    pass

class UserTranslationSchema(UserTranslationBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

