from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from sqlalchemy import select, distinct

from app.core.database import get_db
from app.domain.vocab.models import Language, MasterWord, Domain, Difficulty, Translation
from app.domain.vocab.schemas import LanguageSchema, DomainSchema, MasterWordCreate, MasterWordSchema, TranslationCreate
from fastapi import HTTPException

router = APIRouter()

@router.get("/languages", response_model=List[LanguageSchema])
async def get_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language))
    return result.scalars().all()

@router.get("/domains", response_model=List[DomainSchema])
async def get_domains(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Domain))
    return result.scalars().all()

@router.get("/difficulties", response_model=List[str])
async def get_difficulties():
    # Return enum values
    return [d.value for d in Difficulty]

############### Admin / Creation Endpoints ##################

@router.post("/languages", response_model=LanguageSchema)
async def create_language(lang_in: LanguageSchema, db: AsyncSession = Depends(get_db)):
    # Check existing
    if await db.get(Language, lang_in.code):
         raise HTTPException(status_code=400, detail="Language already exists")
    
    db_obj = Language(code=lang_in.code, name=lang_in.name)
    db.add(db_obj)
    await db.commit()
    return db_obj

@router.post("/domains", response_model=DomainSchema)
async def create_domain(domain_name: str, db: AsyncSession = Depends(get_db)):
    # Check existing
    stmt = select(Domain).where(Domain.name == domain_name)
    existing = (await db.execute(stmt)).scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain already exists")
    
    db_obj = Domain(name=domain_name)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/master-words", response_model=MasterWordSchema)
async def create_master_word(word_in: MasterWordCreate, db: AsyncSession = Depends(get_db)):
    db_obj = MasterWord(
        concept=word_in.concept,
        domain_code=word_in.domain_code,
        difficulty=word_in.difficulty,
        word_type=word_in.word_type,
        image_url=word_in.image_url
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/translations", response_model=dict)
async def create_translation(trans_in: TranslationCreate, db: AsyncSession = Depends(get_db)):
    # Create translation for a master word
    db_obj = Translation(
        master_word_concept=trans_in.master_word_concept,
        text=trans_in.text,
        language_code=trans_in.language_code,
        audio_url=trans_in.audio_url,
        gender=trans_in.gender,
        plural_text=trans_in.plural_text,
        sentence_example=trans_in.sentence_example
    )
    db.add(db_obj)
    try:
        await db.commit()
        await db.refresh(db_obj)
        return {"status": "success", "id": db_obj.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
