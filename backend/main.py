from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Customer Inquiry Backend")

origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
]

print("FRONTEND_ORIGIN:", os.getenv("FRONTEND_ORIGIN"))

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


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/inquiries")
async def submit_inquiry(inquiry: Inquiry):
   
   #PLACEHOLDER FOR BEDROCK INTEGRATION
    print(f"Received inquiry: {inquiry.model_dump()}")
    return {"message": "Inquiry submitted successfully", "data": inquiry.model_dump()}

@app.get("/api/manager/inquiries")
async def get_manager_inquiries():
    
    #PLACEHOLDER FOR RDS INTEGRATION
    initial_inquiries = [
        {"id": 1, "category": "Technical", "urgency": "High", "summary": "Login issue on portal", "email": "john.doe@example.com"},
        {"id": 2, "category": "Billing", "urgency": "Medium", "summary": "Question about recent invoice", "email": "jane.smith@example.com"},
        {"id": 3, "category": "General", "urgency": "Low", "summary": "Feedback on new feature", "email": "bob.johnson@example.com"},
        {"id": 4, "category": "Technical", "urgency": "Medium", "summary": "App crashing on startup", "email": "alice.brown@example.com"},
        {"id": 5, "category": "Sales", "urgency": "High", "summary": "Inquiry about enterprise plan", "email": "charlie.d@example.com"},
    ]
    return {"inquiries": initial_inquiries}
