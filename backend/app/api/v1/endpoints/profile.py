from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from ....core.database import get_db
from ....domain.user.models import User, UserLanguage
from ....domain.user.schemas import (
    UserProfileResponse,
    UserProfileUpdate,
    UserLanguageCreate,
    UserLanguageUpdate,
    UserLanguageResponse
)
from .auth import get_current_user


router = APIRouter()


@router.get("/", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's profile with languages"""
    # Fetch user's languages
    result = await db.execute(
        select(UserLanguage).where(UserLanguage.user_id == current_user.id)
    )
    languages = result.scalars().all()
    
    # Convert to response
    profile_data = {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "native_language": current_user.native_language,
        "oauth_provider": current_user.oauth_provider,
        "full_name": current_user.full_name,
        "picture_url": current_user.picture_url,
        "languages": languages
    }
    
    return profile_data


@router.patch("/", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile"""
    if profile_data.native_language is not None:
        current_user.native_language = profile_data.native_language
    
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    
    await db.commit()
    await db.refresh(current_user)
    
    # Fetch languages
    result = await db.execute(
        select(UserLanguage).where(UserLanguage.user_id == current_user.id)
    )
    languages = result.scalars().all()
    
    profile_data = {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "native_language": current_user.native_language,
        "oauth_provider": current_user.oauth_provider,
        "full_name": current_user.full_name,
        "picture_url": current_user.picture_url,
        "languages": languages
    }
    
    return profile_data


@router.get("/languages", response_model=List[UserLanguageResponse])
async def get_user_languages(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all languages for the current user"""
    result = await db.execute(
        select(UserLanguage).where(UserLanguage.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("/languages", response_model=UserLanguageResponse, status_code=status.HTTP_201_CREATED)
async def add_user_language(
    language_data: UserLanguageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a language to user's profile"""
    # Check if already exists
    result = await db.execute(
        select(UserLanguage).where(
            UserLanguage.user_id == current_user.id,
            UserLanguage.language_code == language_data.language_code
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language already added"
        )
    
    user_language = UserLanguage(
        user_id=current_user.id,
        language_code=language_data.language_code,
        level=language_data.level,
        is_learning=language_data.is_learning
    )
    
    db.add(user_language)
    await db.commit()
    await db.refresh(user_language)
    
    return user_language


@router.patch("/languages/{language_code}", response_model=UserLanguageResponse)
async def update_user_language(
    language_code: str,
    language_data: UserLanguageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a user's language"""
    result = await db.execute(
        select(UserLanguage).where(
            UserLanguage.user_id == current_user.id,
            UserLanguage.language_code == language_code
        )
    )
    user_language = result.scalar_one_or_none()
    
    if not user_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    if language_data.level is not None:
        user_language.level = language_data.level
    
    if language_data.is_learning is not None:
        user_language.is_learning = language_data.is_learning
    
    await db.commit()
    await db.refresh(user_language)
    
    return user_language


@router.delete("/languages/{language_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_language(
    language_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove a language from user's profile"""
    await db.execute(
        delete(UserLanguage).where(
            UserLanguage.user_id == current_user.id,
            UserLanguage.language_code == language_code
        )
    )
    await db.commit()
    
    return None
