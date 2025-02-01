from pydantic import BaseModel  # @ Importing BaseModel from Pydantic to define data validation and serialization.
from typing import Optional, List  # @ Importing Optional and List for type hints.
from datetime import datetime  # @ Importing datetime to handle timestamps.

# @ Base class for FAQ translations, used for validation and serialization.
class FAQTranslationBase(BaseModel):
    language: str  # @ The language code for the translation (e.g., 'hi', 'bn').
    question: str  # @ The translated question text.
    answer: str  # @ The translated answer text.

# @ Inherits from FAQTranslationBase to handle creation of FAQ translations.
class FAQTranslationCreate(FAQTranslationBase):
    pass  # @ No additional fields for creation, just uses the base class.

# @ Inherits from FAQTranslationBase and adds fields for FAQ translation objects.
class FAQTranslation(FAQTranslationBase):
    id: int  # @ The unique identifier for the translation.
    faq_id: int  # @ The FAQ ID to which the translation belongs.

    class Config:
        from_attributes = True  # @ Allows automatic population of model fields from attributes (for ORM compatibility).

# @ Base class for FAQ data, used for validation and serialization.
class FAQBase(BaseModel):
    question_en: str  # @ The original question text in English.
    answer_en: str  # @ The original answer text in English.

# @ Inherits from FAQBase and adds optional translations for FAQ creation.
class FAQCreate(FAQBase):
    translations: Optional[List[FAQTranslationCreate]] = None  # @ A list of translations (optional) when creating an FAQ.

# @ Inherits from FAQBase and adds additional fields for FAQ objects.
class FAQ(FAQBase):
    id: int  # @ The unique identifier for the FAQ.
    created_at: datetime  # @ Timestamp for when the FAQ is created.
    updated_at: datetime  # @ Timestamp for when the FAQ is updated.
    translations: List[FAQTranslation] = []  # @ A list of translations associated with the FAQ.

    class Config:
        from_attributes = True  # @ Allows automatic population of model fields from attributes (for ORM compatibility).
