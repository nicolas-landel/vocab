from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict

from app.core.database import get_db
from app.domain.vocab.models import UserProgress, Word
from app.domain.user.models import User
from pydantic import BaseModel

router = APIRouter()

class UserStats(BaseModel):
    total_words_reviewed: int
    correct_rate: float
    weakest_words: List[str]

@router.get("/", response_model=UserStats)
async def get_user_profile(db: AsyncSession = Depends(get_db)):
    user_id = 1 # Hardcoded for now
    
    # Total Progress
    query = select(UserProgress).where(UserProgress.user_id == user_id)
    progress = (await db.execute(query)).scalars().all()
    
    total_reviewed = len(progress)
    
    total_correct = sum(p.correct_count for p in progress)
    total_attempts = sum(p.correct_count + p.incorrect_count for p in progress)
    
    rate = (total_correct / total_attempts * 100) if total_attempts > 0 else 0.0
    
    # Weakest words (more incorrect than correct, sorted by incorrect count)
    weakest = sorted(progress, key=lambda p: p.incorrect_count, reverse=True)[:5]
    weakest_ids = [p.word_id for p in weakest]
    
    if weakest_ids:
        w_query = select(Word).where(Word.id.in_(weakest_ids))
        words = (await db.execute(w_query)).scalars().all()
        # Maintain order? Hard with IN clause. Map back.
        w_map = {w.id: w.text for w in words}
        weakest_texts = [w_map.get(wid, "Unknown") for wid in weakest_ids]
    else:
        weakest_texts = []
        
    return UserStats(
        total_words_reviewed=total_reviewed,
        correct_rate=round(rate, 2),
        weakest_words=weakest_texts
    )
