from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import os
from dotenv import load_dotenv
import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime


load_dotenv()

app = FastAPI(title="Customer Inquiry Backend")

origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
]
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

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

class InquiryClassification(BaseModel):
    category: Literal["Technical", "Billing", "Sales", "General", "N/A"]
    urgency: Literal["High", "Medium", "Low", "N/A"] 
    summary: str

try:
    model = ChatBedrock(
        model_id="mistral.mistral-small-2402-v1:0",
        region_name="us-east-1",
        model_kwargs={"temperature": 0.1},
    )

    parser = JsonOutputParser(pydantic_object=InquiryClassification)

    prompt = ChatPromptTemplate.from_messages([
    ("system",  "You are an AI assistant that classifies customer inquiries.\n"
            "Decide the correct values strictly based on the inquiry.\n"
            "Valid values:\n"
            "- category: 'Technical', 'Billing', 'Sales', 'General', or 'N/A'\n"
            "- urgency: 'High', 'Medium', 'Low', or 'N/A'\n"
            "- summary: one short sentence.\n\n"
            "Guidelines:\n"
            "- If the inquiry is about bugs, errors, or something not working → 'Technical'.\n"
            "- If it's about invoices, payments, refunds, subscriptions → 'Billing'.\n"
            "- If it's about pricing, plans, discounts, buying something → 'Sales'.\n"
            "- Otherwise → 'General'.\n\n"
            "Do not always default to 'Technical' or 'High'.\n"),
    ("human", "Customer inquiry: {inquiry_text}"),
    ("system", "{format_instructions}"),
])


    chain = prompt | model | parser

except Exception as e:
    print(f"FATAL: Failed to initialize LangChain components on startup: {e}") 

db = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

class InquiryRecord(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    inquiry_text = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    urgency = Column(String(50), nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=db)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/inquiries")
async def submit_inquiry(inquiry: Inquiry, db=Depends(get_db)):
    try:
        classification = chain.invoke({
            "inquiry_text": inquiry.inquiry,
            "format_instructions": parser.get_format_instructions(),
        })
        print(classification)

    except Exception as e:
        print("Error during classification:", e)
        classification = InquiryClassification(
            category="N/A",
            urgency="N/A",
            summary="N/A",
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
        print("DB error while saving inquiry:", e)
        raise HTTPException(status_code=500, detail="Failed to save inquiry to database")  
    
    return {
            "message": "Inquiry classified successfully",
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

    print(inquiries)
    return {"inquiries": inquiries}