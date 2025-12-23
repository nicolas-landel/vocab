# Fixtures Directory Structure

This directory contains seed data for the vocabulary application database.

## Structure

```
fixtures/
├── README.md                          # This file
├── languages.json                     # Global language definitions
├── domains.json                       # Domain definitions with codes
└── <domain_code>/                     # One folder per domain
    ├── master_words.json              # Words for this domain
    ├── translations_en.json           # English translations
    ├── translations_fr.json           # French translations
    └── translations_es.json           # Spanish translations
```

## Domain Folders

Each domain has its own folder named by its code (from `domains.json`):
- `food_dining/` - Food & Dining
- `travel/` - Travel & Transportation
- `daily_life/` - Daily Life
- `work/` - Work & Business
- `health/` - Health & Body
- `family/` - Family & Relationships
- `education/` - Education
- `weather/` - Weather & Nature
- `entertainment/` - Entertainment
- `shopping/` - Shopping

## File Formats

### languages.json
```json
[
  {
    "code": "en",
    "name": "English"
  }
]
```

### domains.json
```json
[
  {
    "id": 1,
    "code": "food_dining",
    "name": "Food & Dining"
  }
]
```

### <domain>/master_words.json
```json
[
  {
    "id": 1,
    "concept": "bread",
    "domain_id": 1,
    "difficulty": "EASY",
    "word_type": "NOUN"
  }
]
```

### <domain>/translations_<lang>.json
```json
[
  {
    "id": 1,
    "master_word_id": 1,
    "language_code": "fr",
    "text": "pain",
    "gender": "masculine",
    "plural_text": "pains",
    "sentence_example": "Le pain est frais."
  }
]
```

## Adding New Vocabulary

To add new vocabulary:

1. Choose the appropriate domain folder
2. Add the word to `master_words.json` with a unique ID
3. Add translations to each `translations_<lang>.json` file
4. Run the seed script: `docker compose exec backend python -m scripts.seed_database`

## Benefits of This Structure

- **Scalability**: Easy to add hundreds or thousands of words without huge files
- **Organization**: Vocabulary grouped by domain
- **Maintainability**: Each domain can be worked on independently
- **i18n Ready**: Domain codes map directly to frontend translations
- **Language Separation**: Each language has its own file per domain
