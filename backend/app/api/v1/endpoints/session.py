from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.domain.vocab.models import Translation, MasterWord, Domain, Difficulty
from app.domain.session.models import Session, SessionWord, SessionType, UserProgress, SessionConfig
from app.domain.session.schemas import (
    SessionConfigCreate, SessionConfigSchema,
    SessionCreate, SessionSchema, SessionDetail,
    SessionWordCreate, SessionWordSchema
)
from app.domain.user.models import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

# Constants
WORDS_PER_DIFFICULTY = {
    "EASY": 10,
    "MEDIUM": 15,
    "HARD": 20
}

# Reusable eager loading options for session details
SESSION_DETAIL_OPTIONS = [
    selectinload(Session.results).selectinload(SessionWord.translation_from).selectinload(Translation.language),
    selectinload(Session.results).selectinload(SessionWord.translation_from).selectinload(Translation.master_word).selectinload(MasterWord.domain),
    selectinload(Session.results).selectinload(SessionWord.translation_to).selectinload(Translation.language),
    selectinload(Session.results).selectinload(SessionWord.translation_to).selectinload(Translation.master_word).selectinload(MasterWord.domain)
]

@router.post("/config", response_model=SessionConfigSchema)
async def create_session_config(
    config_in: SessionConfigCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a session configuration before starting a session"""
    db_config = SessionConfig(
        user_id=current_user.id,
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a new session based on a config"""
    # Get the config
    config = await db.get(SessionConfig, session_in.config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Session config not found")
    
    # Verify the config belongs to the current user
    if config.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to use this config")
    
    # Validate that session input matches config (derive from config for consistency)
    source_lang_code = config.native_language
    target_lang_code = config.language_tested
    domain = config.domain
    difficulty = config.difficulty
    session_type = config.session_type
    
    # Create Session Record
    db_session = Session(
        config_id=config.id,
        user_id=config.user_id,
        source_lang_code=source_lang_code,
        target_lang_code=target_lang_code,
        domain=domain,
        difficulty=difficulty,
        session_type=session_type,
    )
    db.add(db_session)
    await db.flush()  # Flush to get session ID before creating results
    
    # Determine number of words based on difficulty
    num_words = WORDS_PER_DIFFICULTY.get(difficulty, 10)
    
    # Select master words that have translations in BOTH languages
    # This ensures we can always show the word pair
    query = (
        select(MasterWord)
        .join(Translation, Translation.master_word_concept == MasterWord.concept)
        .where(Translation.language_code.in_([source_lang_code, target_lang_code]))
        .group_by(MasterWord.concept)
        .having(func.count(func.distinct(Translation.language_code)) == 2)
    )
    
    # Filter by domain if specified
    if domain and domain != "ALL":
        query = query.where(MasterWord.domain_code == domain)
    
    # Filter by difficulty (cumulative)
    if difficulty:
        if difficulty == "EASY":
            query = query.where(MasterWord.difficulty == Difficulty.EASY)
        elif difficulty == "MEDIUM":
            query = query.where(MasterWord.difficulty.in_([Difficulty.EASY, Difficulty.MEDIUM]))
        elif difficulty == "HARD":
            query = query.where(MasterWord.difficulty.in_([Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]))
    
    # Use SQL random and limit to get random sample efficiently
    query = query.order_by(func.random()).limit(num_words)
    
    selected_master_words = (await db.execute(query)).scalars().all()
    
    if not selected_master_words:
        await db.rollback()
        raise HTTPException(status_code=404, detail="No words found for this configuration")
    
    # Bulk fetch all required translations for selected master words
    concepts = [mw.concept for mw in selected_master_words]
    
    stmt_translations = select(Translation).where(
        Translation.master_word_concept.in_(concepts),
        Translation.language_code.in_([source_lang_code, target_lang_code])
    )
    all_translations = (await db.execute(stmt_translations)).scalars().all()
    
    # Build dictionaries for quick lookup
    translations_by_concept_lang = {}
    for trans in all_translations:
        key = (trans.master_word_concept, trans.language_code)
        translations_by_concept_lang[key] = trans
    
    # Create SessionWord records
    session_words_created = 0
    for master_word in selected_master_words:
        trans_from = translations_by_concept_lang.get((master_word.concept, source_lang_code))
        trans_to = translations_by_concept_lang.get((master_word.concept, target_lang_code))
        
        if trans_from and trans_to:
            res = SessionWord(
                session_id=db_session.id,
                translation_from_id=trans_from.id,
                translation_to_id=trans_to.id,
                from_language=source_lang_code,
                to_language=target_lang_code,
                correct=None
            )
            db.add(res)
            session_words_created += 1
    
    # Ensure we created at least one session word
    if session_words_created == 0:
        await db.rollback()
        raise HTTPException(status_code=422, detail="Could not create session: no valid word pairs found")
    
    await db.commit()
    
    # Reload session with all nested relationships
    stmt = select(Session).where(Session.id == db_session.id).options(*SESSION_DETAIL_OPTIONS)
    result = await db.execute(stmt)
    return result.scalars().first()

@router.post("/{session_id}/submit", response_model=SessionDetail)
async def submit_session(
    session_id: int,
    words: List[SessionWordCreate],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit session results and calculate score"""
    db_session = await db.get(Session, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify the session belongs to the current user
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to submit this session")
    
    if not words:
        raise HTTPException(status_code=422, detail="No words submitted")
    
    # Bulk fetch all SessionWords for this session
    translation_to_ids = [w.translation_to_id for w in words]
    
    stmt_session_words = select(SessionWord).where(
        SessionWord.session_id == session_id,
        SessionWord.translation_to_id.in_(translation_to_ids)
    )
    session_words = (await db.execute(stmt_session_words)).scalars().all()
    session_words_by_id = {sw.translation_to_id: sw for sw in session_words}
    
    # Bulk fetch all UserProgress for these translations
    stmt_progress = select(UserProgress).where(
        UserProgress.user_id == current_user.id,
        UserProgress.translation_id.in_(translation_to_ids)
    )
    progress_records = (await db.execute(stmt_progress)).scalars().all()
    progress_by_id = {up.translation_id: up for up in progress_records}
    
    correct_count = 0
    total = 0
    
    # Update SessionWords and UserProgress in memory
    for r_in in words:
        existing = session_words_by_id.get(r_in.translation_to_id)
        
        if existing:
            existing.correct = r_in.correct
            existing.user_answer = r_in.user_answer
            
            if r_in.correct:
                correct_count += 1
            total += 1
            
            # Update or create UserProgress
            prog = progress_by_id.get(r_in.translation_to_id)
            if not prog:
                prog = UserProgress(
                    user_id=current_user.id,
                    translation_id=r_in.translation_to_id,
                    correct_count=0,
                    incorrect_count=0
                )
                db.add(prog)
                progress_by_id[r_in.translation_to_id] = prog
            
            if r_in.correct:
                prog.correct_count += 1
            else:
                prog.incorrect_count += 1
            
            prog.last_reviewed = datetime.utcnow()
    
    # Update Session score and completion
    score = int((correct_count / total) * 100) if total > 0 else 0
    db_session.score = score
    db_session.completed_at = datetime.utcnow()
    
    await db.commit()
    
    # Return session with all nested relationships
    stmt = select(Session).where(Session.id == db_session.id).options(*SESSION_DETAIL_OPTIONS)
    result = await db.execute(stmt)
    return result.scalars().first()

@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a session with all its results"""
    stmt = select(Session).where(Session.id == session_id).options(*SESSION_DETAIL_OPTIONS)
    result = await db.execute(stmt)
    session = result.scalars().first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify the session belongs to the current user
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session")
    
    return session

@router.get("/", response_model=List[SessionSchema])
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all sessions for the current user"""
    stmt = select(Session).where(Session.user_id == current_user.id).order_by(Session.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

