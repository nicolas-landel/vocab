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
import argparse
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
    await session.commit()


async def load_domains(session: AsyncSession):
    """Load domains from fixtures/domains.json"""
    print("\nLoading domains...")
    with open(FIXTURES_DIR / "domains.json") as f:
        domains_data = json.load(f)
    
    for domain_data in domains_data:
        # Check if already exists
        result = await session.execute(
            select(Domain).where(Domain.code == domain_data["code"])
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            domain = Domain(**domain_data)
            session.add(domain)
        else:
            # Update existing domain
            existing.name = domain_data["name"]    
    await session.commit()


async def load_master_words(session: AsyncSession, domain_code: str = None):
    """Load master words from domain-specific fixture files"""
    print("\nLoading master words...")
    
    # Get all domain folders
    domain_folders = [d for d in FIXTURES_DIR.iterdir() if d.is_dir()]
    
    # Filter by domain_code if provided
    if domain_code:
        domain_folders = [d for d in domain_folders if d.name == domain_code]
        if not domain_folders:
            print(f"  Warning: No domain folder found for '{domain_code}'")
            return
    
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
            else:
                # Update existing word              
                existing.domain_code = word_data["domain_code"]
                existing.difficulty = word_data["difficulty"]
                existing.image_url = word_data.get("image_url")
                existing.word_type = word_data.get("word_type")
    
    await session.commit()


async def load_translations(session: AsyncSession, domain_code: str = None):
    """Load translations from domain and language-specific fixture files"""
    print("\nLoading translations...")
    
    # Get all domain folders
    domain_folders = [d for d in FIXTURES_DIR.iterdir() if d.is_dir()]
    
    # Filter by domain_code if provided
    if domain_code:
        domain_folders = [d for d in domain_folders if d.name == domain_code]
        if not domain_folders:
            print(f"  Warning: No domain folder found for '{domain_code}'")
            return
    
    for domain_folder in sorted(domain_folders):
        # Find all translation files (translations_*.json)
        translation_files = list(domain_folder.glob("translations_*.json"))
        
        if not translation_files:
            continue
            
        print(f"  Loading from {domain_folder.name}...")
        for trans_file in sorted(translation_files):
            lang_code = trans_file.stem.split('_')[1]
            
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
                        Translation.master_word_concept == master_word.concept,
                        Translation.language_code == trans_data["language_code"]
                    )
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    # Create translation with master_word_concept
                    translation_dict = {k: v for k, v in trans_data.items() if k != "concept"}
                    translation_dict["master_word_concept"] = master_word.concept
                    translation = Translation(**translation_dict)
                    session.add(translation)
                    print(f"✓ Added translation: {trans_data['text']} ({lang_code})")
                else:
                    # Update existing translation
                    existing.text = trans_data["text"]
                    existing.audio_url = trans_data.get("audio_url")
                    existing.gender = trans_data.get("gender")
                    existing.plural_text = trans_data.get("plural_text")
                    existing.sentence_example = trans_data.get("sentence_example")
                    existing.synonyms = trans_data.get("synonyms")
    
    await session.commit()


async def seed_database(domain_code: str = None):
    """Main function to seed the database"""
    print("=" * 60)
    if domain_code:
        print(f"Starting database seeding for domain: {domain_code}...")
    else:
        print("Starting database seeding for all domains...")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        try:
            await load_languages(session)
            await load_domains(session)
            await load_master_words(session, domain_code)
            await load_translations(session, domain_code)
            
            print("\n" + "=" * 60)
            print("✓ Database seeding completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n✗ Error during seeding: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed database with fixture data from JSON files."
    )
    parser.add_argument(
        "--domain",
        "-d",
        type=str,
        help="Specific domain code to load (e.g., 'food_dining'). If not provided, all domains will be loaded."
    )
    args = parser.parse_args()
    
    asyncio.run(seed_database(domain_code=args.domain))
