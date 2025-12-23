"""
Seed database with fixture data from JSON files.

The new structure organizes fixtures by domain:
- fixtures/languages.json (global)
- fixtures/domains.json (global)
- fixtures/<domain_code>/master_words.json
- fixtures/<domain_code>/translations_<lang>.json

Usage:
    python -m scripts.seed_database
    
Or from Docker:
    docker compose exec backend python -m scripts.seed_database
"""
import asyncio
import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.domain.vocab.models import Language, Domain, MasterWord, Translation


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


async def load_languages(session: AsyncSession):
    """Load languages from fixtures/languages.json"""
    print("Loading languages...")
    with open(FIXTURES_DIR / "languages.json") as f:
        languages_data = json.load(f)
    
    for lang_data in languages_data:
        # Check if already exists
        result = await session.execute(
            select(Language).where(Language.code == lang_data["code"])
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            language = Language(**lang_data)
            session.add(language)
            print(f"  ✓ Added language: {lang_data['name']}")
        else:
            print(f"  - Skipped (exists): {lang_data['name']}")
    
    await session.commit()


async def load_domains(session: AsyncSession):
    """Load domains from fixtures/domains.json"""
    print("\nLoading domains...")
    with open(FIXTURES_DIR / "domains.json") as f:
        domains_data = json.load(f)
    
    for domain_data in domains_data:
        # Check if already exists
        result = await session.execute(
            select(Domain).where(Domain.id == domain_data["id"])
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            domain = Domain(**domain_data)
            session.add(domain)
            print(f"  ✓ Added domain: {domain_data['name']}")
        else:
            print(f"  - Skipped (exists): {domain_data['name']}")
    
    await session.commit()


async def load_master_words(session: AsyncSession):
    """Load master words from domain-specific fixture files"""
    print("\nLoading master words...")
    
    # Get all domain folders
    domain_folders = [d for d in FIXTURES_DIR.iterdir() if d.is_dir()]
    
    for domain_folder in sorted(domain_folders):
        master_words_file = domain_folder / "master_words.json"
        if not master_words_file.exists():
            continue
            
        with open(master_words_file) as f:
            words_data = json.load(f)
        
        if not words_data:  # Skip empty files
            continue
            
        print(f"  Loading from {domain_folder.name}...")
        for word_data in words_data:
            # Check if already exists by concept
            result = await session.execute(
                select(MasterWord).where(MasterWord.concept == word_data["concept"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                master_word = MasterWord(**word_data)
                session.add(master_word)
                print(f"    ✓ Added word: {word_data['concept']}")
            else:
                print(f"    - Skipped (exists): {word_data['concept']}")
    
    await session.commit()


async def load_translations(session: AsyncSession):
    """Load translations from domain and language-specific fixture files"""
    print("\nLoading translations...")
    
    # Get all domain folders
    domain_folders = [d for d in FIXTURES_DIR.iterdir() if d.is_dir()]
    
    for domain_folder in sorted(domain_folders):
        # Find all translation files (translations_*.json)
        translation_files = list(domain_folder.glob("translations_*.json"))
        
        if not translation_files:
            continue
            
        print(f"  Loading from {domain_folder.name}...")
        for trans_file in sorted(translation_files):
            lang_code = trans_file.stem.split('_')[1]  # Extract language code from filename
            
            with open(trans_file) as f:
                translations_data = json.load(f)
            
            if not translations_data:  # Skip empty files
                continue
                
            for trans_data in translations_data:
                # Find the master word by concept
                result = await session.execute(
                    select(MasterWord).where(MasterWord.concept == trans_data["concept"])
                )
                master_word = result.scalar_one_or_none()
                
                if not master_word:
                    print(f"    ✗ Master word not found for concept: {trans_data['concept']}")
                    continue
                
                # Check if translation already exists for this master_word + language
                result = await session.execute(
                    select(Translation).where(
                        Translation.master_word_id == master_word.id,
                        Translation.language_code == trans_data["language_code"]
                    )
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    # Create translation with master_word_id
                    translation_dict = {k: v for k, v in trans_data.items() if k != "concept"}
                    translation_dict["master_word_id"] = master_word.id
                    translation = Translation(**translation_dict)
                    session.add(translation)
                    print(f"    ✓ Added translation: {trans_data['text']} ({lang_code})")
                else:
                    print(f"    - Skipped (exists): {trans_data['text']} ({lang_code})")
    
    await session.commit()


async def seed_database():
    """Main function to seed the database"""
    print("=" * 60)
    print("Starting database seeding...")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        try:
            await load_languages(session)
            await load_domains(session)
            await load_master_words(session)
            await load_translations(session)
            
            print("\n" + "=" * 60)
            print("✓ Database seeding completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n✗ Error during seeding: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())
