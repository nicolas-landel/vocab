from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from sqlalchemy import select, distinct

from app.core.database import get_db
from app.domain.vocab.models import Language, Word, Difficulty, Translation
from app.domain.vocab.schemas import LanguageSchema, WordCreate, WordSchema, TranslationCreate
from fastapi import HTTPException

router = APIRouter()

@router.get("/languages", response_model=List[LanguageSchema])
async def get_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language))
    return result.scalars().all()

@router.get("/domains", response_model=List[str])
async def get_domains(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(distinct(Word.domain)))
    return result.scalars().all()

@router.get("/difficulties", response_model=List[str])
async def get_difficulties():
    # Return enum values
    return [d.value for d in Difficulty]

# --- Admin / Creation Endpoints ---

@router.post("/languages", response_model=LanguageSchema)
async def create_language(lang_in: LanguageSchema, db: AsyncSession = Depends(get_db)):
    # Check existing
    if await db.get(Language, lang_in.code):
         raise HTTPException(status_code=400, detail="Language already exists")
    
    db_obj = Language(code=lang_in.code, name=lang_in.name)
    db.add(db_obj)
    await db.commit()
    return db_obj

@router.post("/words", response_model=WordSchema)
async def create_word(word_in: WordCreate, db: AsyncSession = Depends(get_db)):
    db_obj = Word(
        text=word_in.text,
        language_code=word_in.language_code,
        domain=word_in.domain,
        difficulty=word_in.difficulty
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/translations", response_model=dict)
async def create_translation(trans_in: TranslationCreate, db: AsyncSession = Depends(get_db)):
    # Simple link
    db_obj = Translation(
        source_word_id=trans_in.source_word_id, 
        target_word_id=trans_in.target_word_id
    )
    db.add(db_obj)
    try:
        await db.commit()
        return {"status": "success", "id": db_obj.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
