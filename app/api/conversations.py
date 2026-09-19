from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.database import Conversation, Message
from app.models.environmental import EnvironmentalProfile

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("/{conversation_id}")
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = [
        {"id": m.id, "sender": m.sender, "content": m.content, "timestamp": m.timestamp.isoformat()}
        for m in conv.messages
    ]

    profile_dict = {}
    if conv.profile:
        for k in EnvironmentalProfile.model_fields.keys():
            if hasattr(conv.profile, k):
                profile_dict[k] = getattr(conv.profile, k)

    return {
        "conversation_id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat(),
        "updated_at": conv.updated_at.isoformat(),
        "messages": messages,
        "environmental_profile": profile_dict
    }

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conv)
    db.commit()
    return {"status": "deleted", "conversation_id": conversation_id}
