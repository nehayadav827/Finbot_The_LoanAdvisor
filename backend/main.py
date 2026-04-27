from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

from agents.master_agent import MasterAgent
from services.session_store import SessionStore

app = FastAPI(title="FinBot API", version="1.0.0")

# In production set ALLOWED_ORIGINS env var on Render to your Vercel URL
# e.g. ALLOWED_ORIGINS=https://finbot-xyz.vercel.app
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
origins = [o.strip() for o in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_store = SessionStore()

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    stage: str
    loan_data: Optional[dict] = None
    sanction_url: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    session = session_store.get_or_create(session_id)
    
    agent = MasterAgent(session, session_store)
    result = await agent.process(req.message)
    
    return ChatResponse(
        session_id=session_id,
        reply=result["reply"],
        stage=result["stage"],
        loan_data=result.get("loan_data"),
        sanction_url=result.get("sanction_url"),
    )

@app.get("/session/{session_id}")
def get_session(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.delete("/session/{session_id}")
def reset_session(session_id: str):
    session_store.delete(session_id)
    return {"status": "reset"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)