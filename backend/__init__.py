"""
Rajasthan Technical Education Chatbot Backend
Initializes the application and sets up core configurations
"""

from .config import settings
from .database import init_db

# Perform any necessary initialization
init_db()