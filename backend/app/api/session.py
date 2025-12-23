from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload
from typing import List
import random
from datetime import datetime

from app.core.database import get_db
from app.domain.vocab.models import Translation, MasterWord, Domain, Difficulty
from app.domain.session.models import Session, SessionResult, SessionType, UserProgress, SessionConfig
from app.domain.session.schemas import (
    SessionConfigCreate, SessionConfigSchema,
    SessionCreate, SessionSchema, SessionDetail,
    SessionResultCreate, SessionResultSchema
)
from app.domain.user.models import User

router = APIRouter()

@router.post("/config", response_model=SessionConfigSchema)
async def create_session_config(
    config_in: SessionConfigCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Create a session configuration before starting a session"""
    # For now, hardcode user_id=1. In real app, get from current_user
    user = await db.get(User, 1)
    if not user:
        raise HTTPException(status_code=400, detail="User not found. Please seed data.")
    
    db_config = SessionConfig(
        user_id=user.id,
        native_language=config_in.native_language,
        language_tested=config_in.language_tested,
        difficulty=config_in.difficulty,
        domain=config_in.domain,
        session_type=config_in.session_type
    )
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    
    return db_config

@router.post("/start", response_model=SessionDetail)
async def start_session(
    session_in: SessionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Start a new session based on a config"""
    # Get the config
    config = await db.get(SessionConfig, session_in.config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Session config not found")
    
    # Create Session Record
    db_session = Session(
        config_id=config.id,
        user_id=config.user_id,
        source_lang_code=session_in.source_lang_code,
        target_lang_code=session_in.target_lang_code,
        domain=session_in.domain,
        difficulty=session_in.difficulty,
        session_type=session_in.session_type,
    )
    db.add(db_session)
    await db.flush()
    
    # Select translations based on criteria
    # We want translations in the target language (language being tested)
    query = select(Translation).join(MasterWord).where(
        Translation.language_code == session_in.target_lang_code
    )
    
    # Filter by domain if specified
    if session_in.domain:
        query = query.join(Domain).where(Domain.name == session_in.domain)
    
    # Filter by difficulty if specified
    if session_in.difficulty:
        query = query.where(MasterWord.difficulty == session_in.difficulty)
    
    translations = (await db.execute(query)).scalars().all()
    
    if not translations:
        raise HTTPException(status_code=404, detail="No words found for this configuration")

    # Random selection of 5-10 words
    num_words = min(len(translations), 10)
    selected_translations = random.sample(translations, num_words)
    
    # Create empty results for these translations
    for trans in selected_translations:
        res = SessionResult(
            session_id=db_session.id,
            translation_id=trans.id,
            correct=False  # Will be updated when user submits
        )
        db.add(res)
        
    await db.commit()
    
    # Reload session with results
    stmt = select(Session).where(Session.id == db_session.id).options(
        selectinload(Session.results).selectinload(SessionResult.translation)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

@router.post("/{session_id}/submit", response_model=SessionDetail)
async def submit_session(
    session_id: int, 
    results: List[SessionResultCreate], 
    db: AsyncSession = Depends(get_db)
):
    """Submit session results and calculate score"""
    db_session = await db.get(Session, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    correct_count = 0
    total = 0
    
    for r_in in results:
         # Find result row for this session & translation
         stmt = select(SessionResult).where(
             SessionResult.session_id == session_id, 
             SessionResult.translation_id == r_in.translation_id
         )
         existing = (await db.execute(stmt)).scalars().first()
         
         if existing:
             existing.correct = r_in.correct
             if r_in.correct:
                 correct_count += 1
             total += 1
             
             # Update UserProgress
             stmt_prog = select(UserProgress).where(
                 UserProgress.user_id == db_session.user_id, 
                 UserProgress.translation_id == r_in.translation_id
             )
             prog = (await db.execute(stmt_prog)).scalars().first()
             
             if not prog:
                 prog = UserProgress(
                     user_id=db_session.user_id, 
                     translation_id=r_in.translation_id
                 )
                 db.add(prog)
            
             if r_in.correct:
                 prog.correct_count += 1
             else:
                 prog.incorrect_count += 1
             
             prog.last_reviewed = datetime.utcnow()
                 
    # Update Session Score and mark as completed
    score = int((correct_count / total) * 100) if total > 0 else 0
    db_session.score = score
    db_session.completed_at = datetime.utcnow()
    
    await db.commit()
    
    # Return session with results
    stmt = select(Session).where(Session.id == db_session.id).options(
        selectinload(Session.results).selectinload(SessionResult.translation)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get a session with all its results"""
    stmt = select(Session).where(Session.id == session_id).options(
        selectinload(Session.results).selectinload(SessionResult.translation)
    )
    result = await db.execute(stmt)
    session = result.scalars().first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.get("/", response_model=List[SessionSchema])
async def get_user_sessions(db: AsyncSession = Depends(get_db)):
    """Get all sessions for the current user"""
    # Hardcoded user for now
    user_id = 1
    
    stmt = select(Session).where(Session.user_id == user_id).order_by(Session.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

