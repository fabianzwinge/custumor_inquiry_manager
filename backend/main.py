from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from database import get_db, InquiryRecord, init_db
from bedrock_llm import chain, parser, InquiryClassification
from ses import send_confirmation_email, send_response_email

load_dotenv()

init_db()

app = FastAPI(title="Customer Inquiry Backend")

origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Inquiry(BaseModel):
    name: str
    email: str
    inquiry: str

class InquiryResponse(BaseModel):
    response: str


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/inquiries")
async def submit_inquiry(inquiry: Inquiry, db=Depends(get_db)):
    classification = None
    if chain and parser:
        try:
            classification = chain.invoke({
                "inquiry_text": inquiry.inquiry,
                "format_instructions": parser.get_format_instructions(),
            })
            print(classification)
        except Exception as e:
            print(f"Error during classification: {e}")
    
    if not classification:
        classification = InquiryClassification(
            category="N/A",
            urgency="N/A",
            summary="Classification failed.",
        )

    try:
        record = InquiryRecord(
            name=inquiry.name,
            email=inquiry.email,
            inquiry_text=inquiry.inquiry,
            category=classification["category"],
            urgency=classification["urgency"],
            summary=classification["summary"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        print(f"DB error while saving inquiry: {e}")
        raise HTTPException(status_code=500, detail="Failed to save inquiry to database")
    
    send_confirmation_email(
        to_address=record.email,
        name=record.name,
        inquiry_id=record.id,
        inquiry_text=record.inquiry_text
    )
    
    return {
        "message": "Inquiry classified and confirmation email sent successfully",
        "data": inquiry.model_dump(),
        "classification": classification,
    }

@app.get("/api/manager/inquiries")
async def get_manager_inquiries(db=Depends(get_db)):
    records = db.query(InquiryRecord).order_by(InquiryRecord.created_at.desc()).all()
    inquiries = [
        {
            "id": r.id,
            "name": r.name,
            "email": r.email,
            "inquiry": r.inquiry_text,
            "category": r.category,
            "urgency": r.urgency,
            "summary": r.summary,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]
    return {"inquiries": inquiries}

@app.get("/api/inquiries/{inquiry_id}")
async def get_inquiry_by_id(inquiry_id: int, db=Depends(get_db)):
    record = db.query(InquiryRecord).filter(InquiryRecord.id == inquiry_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {
        "id": record.id,
        "name": record.name,
        "email": record.email,
        "inquiry": record.inquiry_text,
        "category": record.category,
        "urgency": record.urgency,
        "summary": record.summary,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }

@app.post("/api/inquiries/{inquiry_id}/respond")
async def respond_to_inquiry(inquiry_id: int, response: InquiryResponse, db=Depends(get_db)):
    record = db.query(InquiryRecord).filter(InquiryRecord.id == inquiry_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    print(f"Response for inquiry {inquiry_id}: {response.response}")

    message_id = send_response_email(
        to_address=record.email,
        inquiry_id=inquiry_id,
        response_text=response.response,
        inquiry_text=record.inquiry_text
    )

    if message_id:
        return {"message": "Response submitted and email sent successfully", "emailMessageId": message_id}
    else:
        raise HTTPException(status_code=500, detail="Response submitted but failed to send email.")