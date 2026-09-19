from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
def handle_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    service = ConversationService(db)
    return service.process_user_turn(
        conversation_id=payload.conversation_id,
        user_message=payload.message,
        profile_override=payload.profile_override
    )
