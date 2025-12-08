from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from typing import List
import random

from app.core.database import get_db
from app.domain.vocab import Word, Translation, Difficulty, UserProgress
from app.domain.session.models import Session, SessionResult, SessionType
from app.domain.session.schemas import SessionCreate, SessionSchema, SessionResultSchema, SessionResultCreate
from app.domain.user.models import User

# Remove Old Import

router = APIRouter()

@router.post("/start", response_model=SessionSchema)
async def start_session(session_in: SessionCreate, db: AsyncSession = Depends(get_db)):
    # 1. Create Session Record
    # For now, hardcode user_id=1. In real app, get from current_user
    user = await db.get(User, 1)
    if not user:
        raise HTTPException(status_code=400, detail="User not found. Please seed data.")
        
    db_session = Session(
        user_id=user.id,
        source_lang_code=session_in.source_lang_code,
        target_lang_code=session_in.target_lang_code,
        domain=session_in.domain,
        difficulty=session_in.difficulty,
        session_type=session_in.session_type,
    )
    db.add(db_session)
    await db.flush()
    
    # 2. Select Words
    # Find words in SOURCE lang that have a translation in TARGET lang.
    # We check both directions in Translation table to be safe.
    
    # Aliases to join Translation twice?
    # Simpler: Get all words in Source Lang compatible with domain/diff.
    # Then filter key ones that have translation.
    
    query = select(Word).where(Word.language_code == session_in.source_lang_code)
    
    if session_in.domain:
        query = query.where(Word.domain == session_in.domain)
        
    words = (await db.execute(query)).scalars().all()
    
    valid_words = []
    
    # This loop is N+1 but efficient enough for small vocab. 
    # For production, use JOINs.
    for w in words:
        # Check if translation exists to target lang
        # Case 1: w is source in Translation, target is in TargetLang
        # Case 2: w is target in Translation, source is in TargetLang
        
        t_query = select(Translation).join(Word, Translation.target_word_id == Word.id).where(
            Translation.source_word_id == w.id,
            Word.language_code == session_in.target_lang_code
        )
        res1 = (await db.execute(t_query)).first()
        
        if res1:
            valid_words.append(w)
            continue
            
        t_query2 = select(Translation).join(Word, Translation.source_word_id == Word.id).where(
            Translation.target_word_id == w.id,
            Word.language_code == session_in.target_lang_code
        )
        res2 = (await db.execute(t_query2)).first()
        
        if res2:
            valid_words.append(w)

    if not valid_words:
        raise HTTPException(status_code=404, detail="No words found for this configuration")

    # Random selection of 5 words
    selected_words = random.sample(valid_words, min(len(valid_words), 5))
    
    # Create empty results for these words
    for w in selected_words:
        res = SessionResult(
            session_id=db_session.id,
            word_id=w.id,
            correct=False 
        )
        db.add(res)
        
    await db.commit()
    # Reload session with results
    stmt = select(Session).where(Session.id == db_session.id).options(
        selectinload(Session.results).selectinload(SessionResult.word)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

@router.post("/{session_id}/submit", response_model=SessionSchema)
async def submit_session(session_id: int, results: List[SessionResultCreate], db: AsyncSession = Depends(get_db)):
    db_session = await db.get(Session, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    correct_count = 0
    total = 0
    
    for r_in in results: # Iterate inputs
         # Find matching result in DB or create if submitting partial?
         # Typically we update the existing rows created at start.
         # But schema has word_id in input.
         
         # Let's assume we update the result rows
         # Find result row for this session & word
         stmt = select(SessionResult).where(SessionResult.session_id == session_id, SessionResult.word_id == r_in.word_id)
         existing = (await db.execute(stmt)).scalars().first()
         
         if existing:
             existing.correct = r_in.correct
             if r_in.correct:
                 correct_count += 1
             total += 1
             
             # Update UserProgress
             # Find or Create progress
             stmt_prog = select(UserProgress).where(UserProgress.user_id == db_session.user_id, UserProgress.word_id == r_in.word_id)
             prog = (await db.execute(stmt_prog)).scalars().first()
             
             if not prog:
                 prog = UserProgress(user_id=db_session.user_id, word_id=r_in.word_id)
                 db.add(prog)
            
             if r_in.correct:
                 prog.correct_count += 1
             else:
                 prog.incorrect_count += 1
                 
    # Update Session Score
    score = int((correct_count / total) * 100) if total > 0 else 0
    db_session.score = score
    
    await db.commit()
    
    stmt = select(Session).where(Session.id == db_session.id).options(
        selectinload(Session.results).selectinload(SessionResult.word)
    )
    result = await db.execute(stmt)
    return result.scalars().first()
