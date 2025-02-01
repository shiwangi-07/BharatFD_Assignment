from fastapi import FastAPI, Depends, HTTPException, Query  # @ Importing necessary FastAPI functions and types.
from sqlalchemy.orm import Session  # @ Importing SQLAlchemy session management tools.
from typing import List  # @ Importing the List type for type hints.
import json  # @ Importing JSON library for encoding and decoding data.

from . import models, schemas, translation  # @ Importing models, schemas, and translation logic from the local package.
from .database import engine, get_db, redis_client  # @ Importing database engine, db session getter, and Redis client.

# @ Creating all database tables defined in the models. `Base.metadata.create_all` binds the engine to the models.
models.Base.metadata.create_all(bind=engine)

# @ Initializing the FastAPI application with a title.
app = FastAPI(title="Multilingual FAQ System")

# @ Endpoint to create a new FAQ. It receives an FAQ creation schema and saves the data to the database.
@app.post("/faqs/", response_model=schemas.FAQ)
async def create_faq(faq: schemas.FAQCreate, db: Session = Depends(get_db)):
    # @ Creating a new FAQ record in the database using the input data.
    db_faq = models.FAQ(
        question_en=faq.question_en,
        answer_en=faq.answer_en
    )
    db.add(db_faq)  # @ Adding the new FAQ to the session.
    db.commit()  # @ Committing the transaction to save the FAQ to the database.
    db.refresh(db_faq)  # @ Refreshing the FAQ object to get the latest state from the database.
    
    # @ Auto-translate the FAQ into supported languages.
    supported_langs = ['hi', 'bn']  # @ List of supported languages for translation.
    for lang in supported_langs:
        trans = models.FAQTranslation(
            faq_id=db_faq.id,  # @ Link the translation to the created FAQ.
            language=lang,
            question=translation.translate_text(faq.question_en, lang),  # @ Translate the question.
            answer=translation.translate_text(faq.answer_en, lang)  # @ Translate the answer.
        )
        db.add(trans)  # @ Adding the translation to the session.
    
    db.commit()  # @ Commit the transaction to save translations.
    db.refresh(db_faq)  # @ Refresh the FAQ object again.
    return db_faq  # @ Returning the created FAQ object.

# @ Endpoint to fetch FAQs. It allows for pagination, language selection, and uses Redis caching.
@app.get("/faqs/", response_model=List[schemas.FAQ])
async def get_faqs(
    skip: int = 0,  # @ Pagination parameter: how many records to skip.
    limit: int = 10,  # @ Pagination parameter: how many records to limit.
    lang: str = Query(None, max_length=2),  # @ Language query parameter for fetching specific language translations.
    db: Session = Depends(get_db)  # @ Dependency injection for the database session.
):
    # @ Try to fetch the FAQs from the Redis cache using the language and pagination as the cache key.
    cache_key = f"faqs:{lang}:{skip}:{limit}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        # @ If cache exists, return the cached data after loading it as JSON.
        return json.loads(cached_data)
    
    # @ If no cache, fetch the FAQs from the database.
    faqs = db.query(models.FAQ).offset(skip).limit(limit).all()
    
    # @ If a specific language is requested, ensure the translations are loaded or created.
    if lang and lang != 'en':
        for faq in faqs:
            # @ Check if translation for the specified language already exists.
            if not any(t.language == lang for t in faq.translations):
                # @ If translation does not exist, create a new one.
                trans = models.FAQTranslation(
                    faq_id=faq.id,
                    language=lang,
                    question=translation.translate_text(faq.question_en, lang),
                    answer=translation.translate_text(faq.answer_en, lang)
                )
                db.add(trans)  # @ Add the translation to the session.
        db.commit()  # @ Commit the new translations.
    
    # @ Cache the FAQ results in Redis for 5 minutes.
    redis_client.setex(
        cache_key,  # @ Cache key is based on language and pagination.
        300,  # @ Cache duration in seconds (5 minutes).
        json.dumps([{
            "id": faq.id,
            "question_en": faq.question_en,
            "answer_en": faq.answer_en,
            "created_at": faq.created_at.isoformat(),  # @ Convert datetime to ISO format for JSON serialization.
            "updated_at": faq.updated_at.isoformat(),  # @ Convert datetime to ISO format.
            "translations": [{
                "id": t.id,
                "faq_id": t.faq_id,
                "language": t.language,
                "question": t.question,
                "answer": t.answer
            } for t in faq.translations]  # @ Include translations for each FAQ.
        } for faq in faqs])
    )
    
    return faqs  # @ Return the list of FAQs (with or without translations).
