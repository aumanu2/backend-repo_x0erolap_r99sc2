from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from database import create_document, db

app = FastAPI(title="Nabil Karim Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactPayload(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=5, max_length=5000)


@app.get("/test")
async def test():
    try:
        if db is not None:
            db.command("ping")
            db_ok = True
        else:
            db_ok = False
        return {"status": "ok", "database": db_ok}
    except Exception as e:
        return {"status": "ok", "database": False, "error": str(e)}


@app.post("/contact")
async def submit_contact(payload: ContactPayload):
    try:
        doc_id = create_document("contactmessage", payload.model_dump())
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Portfolio API running"}
