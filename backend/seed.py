import asyncio
from app.core.database import AsyncSessionLocal
from app.domain.vocab.models import Language, Word, Difficulty, Translation

async def seed_data():
    async with AsyncSessionLocal() as session:
        # User
        from app.domain.user.models import User
        from app.core.security import get_password_hash
        
        if not await session.get(User, 1):
             user = User(email="test@example.com", hashed_password=get_password_hash("password"))
             session.add(user)
             await session.flush()
             print("User seeded.")

        # Check if languages exist
        if await session.get(Language, "fr"):
            print("Language data already exists. Skipping vocab seed.")
            await session.commit()
            return


        # Languages
        fr = Language(code="fr", name="French")
        es = Language(code="es", name="Spanish")
        en = Language(code="en", name="English")
        session.add_all([fr, es, en])
        await session.flush()

        # Words (FR) - Travel
        words_fr = [
            Word(text="Voiture", language_code="fr", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Train", language_code="fr", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Avion", language_code="fr", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Billet", language_code="fr", domain="travel", difficulty=Difficulty.MEDIUM),
            Word(text="Valise", language_code="fr", domain="travel", difficulty=Difficulty.MEDIUM),
        ]
        
        # Words (ES) - Travel
        words_es = [
            Word(text="Coche", language_code="es", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Tren", language_code="es", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Avión", language_code="es", domain="travel", difficulty=Difficulty.EASY),
            Word(text="Billete", language_code="es", domain="travel", difficulty=Difficulty.MEDIUM),
            Word(text="Maleta", language_code="es", domain="travel", difficulty=Difficulty.MEDIUM),
        ]

        session.add_all(words_fr + words_es)
        await session.flush()

        # Translations
        # Assuming order matches for simplicity in this seed script
        for w1, w2 in zip(words_fr, words_es):
            t1 = Translation(source_word_id=w1.id, target_word_id=w2.id)
            # We strictly need one direction in DB? Or both?
            # Model has source/target. Logic usually checks both ways or normalized.
            # Let's add just one link pair for now.
            session.add(t1)
        
        await session.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
