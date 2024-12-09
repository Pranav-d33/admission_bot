"""
Chat Router Module
Handles chat-related API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from ..services.chatbot_service import ChatbotService

# Create router
chat_router = APIRouter(tags=["Chat"])

class ChatRequest(BaseModel):
    """
    Input model for chat requests
    Validates incoming chat message
    """
    message: str
    user_id: str = None

class ChatResponse(BaseModel):
    """
    Output model for chat responses
    Standardizes response format
    """
    message: str
    type: str = "text"
    metadata: Dict[str, Any] = {}

@chat_router.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest) -> ChatResponse:
    """
    Process incoming chat messages
    
    Args:
        request (ChatRequest): Incoming chat message
    
    Returns:
        ChatResponse: Processed chatbot response
    
    Raises:
        HTTPException: For processing errors
    """
    try:
        # Process message through chatbot service
        result = ChatbotService.process_query(
            request.message, 
            user_id=request.user_id
        )
        
        return ChatResponse(
            message=result['response'],
            type=result.get('type', 'text'),
            metadata=result.get('metadata', {})
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Chat processing error: {str(e)}"
        )