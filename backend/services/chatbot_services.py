"""
Chatbot Service Module
Implements core chatbot logic with NLP processing
"""

import spacy
import nltk
from typing import Dict, Any, Optional
import logging

from ..database import DatabaseManager
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

class ChatbotService:
    """
    Core chatbot processing service
    Handles query understanding, matching, and response generation
    """
    
    # Load spaCy language model
    _nlp = spacy.load("en_core_web_sm")
    
    @classmethod
    def preprocess_query(cls, query: str) -> str:
        """
        Preprocess user query for semantic matching
        
        Args:
            query (str): Raw user input
        
        Returns:
            str: Processed query tokens
        """
        doc = cls._nlp(query.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        return " ".join(tokens)
    
    @classmethod
    def process_query(
        cls, 
        query: str, 
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Primary method to process user queries
        
        Args:
            query (str): User's input message
            user_id (Optional[str]): Unique user identifier
        
        Returns:
            Dict[str, Any]: Processed response
        """
        try:
            # Preprocess query
            processed_query = cls.preprocess_query(query)
            
            # Get database connection
            db = DatabaseManager.get_database()
            
            # Search FAQs
            faq_match = db.faqs.find_one(
                {"$text": {"$search": processed_query}},
                {"score": {"$meta": "textScore"}}
            )
            
            if faq_match:
                return {
                    "response": faq_match.get("answer", "I found a relevant FAQ but no answer was available."),
                    "type": "faq",
                    "metadata": {"faq_id": str(faq_match.get("_id"))}
                }
            
            # Search Colleges
            college_match = db.colleges.find_one(
                {"$text": {"$search": processed_query}},
                {"score": {"$meta": "textScore"}}
            )
            
            if college_match:
                return {
                    "response": f"About {college_match.get('name', 'College')}: {college_match.get('description', 'No details available.')}",
                    "type": "college_info",
                    "metadata": {"college_id": str(college_match.get("_id"))}
                }
            
            # Default response
            return {
                "response": "I couldn't find specific information. Could you rephrase or be more specific?",
                "type": "default"
            }
        
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return {
                "response": "Sorry, I'm having trouble processing your request right now.",
                "type": "error"
            }