from datetime import datetime  # @ Importing datetime to handle timestamps.
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey  # @ Importing SQLAlchemy types for the columns.
from sqlalchemy.orm import relationship  # @ Importing relationship to define relationships between tables.
from .database import Base  # @ Importing the Base class from the database module to define models.

# @ Defining the FAQ model (table) for storing FAQ data.
class FAQ(Base):
    __tablename__ = "faqs"  # @ The name of the table in the database.
    
    id = Column(Integer, primary_key=True, index=True)  # @ Primary key for the FAQ table, indexed for efficient querying.
    question_en = Column(Text, nullable=False)  # @ Column to store the FAQ question in English (mandatory).
    answer_en = Column(Text, nullable=False)  # @ Column to store the FAQ answer in English (mandatory).
    created_at = Column(DateTime, default=datetime.utcnow)  # @ Timestamp for when the FAQ is created.
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # @ Timestamp for when the FAQ is updated, auto-updated on modification.
    
    # @ Relationship to the FAQTranslation table, establishing a one-to-many relationship (one FAQ can have many translations).
    translations = relationship("FAQTranslation", back_populates="faq", cascade="all, delete-orphan")  # @ Cascade ensures that if an FAQ is deleted, its translations are also deleted.

# @ Defining the FAQTranslation model (table) for storing translations of FAQ data.
class FAQTranslation(Base):
    __tablename__ = "faq_translations"  # @ The name of the table in the database.
    
    id = Column(Integer, primary_key=True, index=True)  # @ Primary key for the FAQTranslation table, indexed for efficient querying.
    faq_id = Column(Integer, ForeignKey("faqs.id", ondelete="CASCADE"))  # @ Foreign key linking to the FAQ table, with cascading delete.
    language = Column(String(2), nullable=False)  # @ Column to store the language code (e.g., 'hi', 'bn') of the translation (mandatory).
    question = Column(Text, nullable=False)  # @ Column to store the translated question (mandatory).
    answer = Column(Text, nullable=False)  # @ Column to store the translated answer (mandatory).
    
    # @ Relationship to the FAQ table, establishing a back-reference to the FAQ.
    faq = relationship("FAQ", back_populates="translations")  # @ Using back_populates to link to the translations attribute in the FAQ class.
