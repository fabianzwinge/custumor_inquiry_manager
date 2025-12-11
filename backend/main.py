from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import os
from dotenv import load_dotenv
import json

from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


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

class InquiryClassification(BaseModel):
    category: Literal["Technical", "Billing", "Sales", "General", "N/A"]
    urgency: Literal["High", "Medium", "Low", "N/A"] 
    summary: str

try:
    model = ChatBedrock(
        model_id="amazon.titan-text-lite-v1",
        model_kwargs={"temperature": 0.1},
    )

    parser = JsonOutputParser(pydantic_object=InquiryClassification)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant that classifies customer inquiries. Respond with a JSON object containing 'category', 'urgency', and 'summary'. The category must be one of 'Technical', 'Billing', 'Sales', or 'General'. The urgency must be one of 'High', 'Medium', or 'Low'. The summary should be a single sentence. If you cannot determine a value, use 'N/A'."),
        ("human", "Customer inquiry: {inquiry_text}"),
        ("system", "{format_instructions}"),
    ])

    chain = prompt | model | parser

except Exception as e:
    print(f"FATAL: Failed to initialize LangChain components on startup: {e}") 

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/inquiries")
async def submit_inquiry(inquiry: Inquiry):
    if chain is None:
        raise HTTPException(status_code=500, detail="LangChain components not initialized. Check server logs.")
    
    try:
        classification = await chain.ainvoke({
            "inquiry_text": inquiry.inquiry,
            "format_instructions": parser.get_format_instructions(),
        })
        
        print(classification)

        #PLACEHOLDER FOR RDS INTEGRATION
        return {
            "message": "Inquiry classified successfully",
            "data": inquiry.model_dump(),
            "classification": classification,
        }

    except Exception as e:
        print("Error during inquiry submission:", e)
        raise HTTPException(status_code=500, detail="Failed to process inquiry with LangChain.")
    
@app.get("/api/manager/inquiries")
async def get_manager_inquiries():
    
    #PLACEHOLDER FOR RDS INTEGRATION
    initial_inquiries = [
        {"id": 1, "category": "Technical", "urgency": "High", "summary": "Login issue on portal", "email": "john.doe@example.com"},
        {"id": 2, "category": "Billifng", "urgency": "Medium", "summary": "Question about recent invoice", "email": "jane.smith@example.com"},
        {"id": 3, "category": "General", "urgency": "Low", "summary": "Feedback on new feature", "email": "bob.johnson@example.com"},
        {"id": 4, "category": "Technical", "urgency": "Medium", "summary": "App crashing on startup", "email": "alice.brown@example.com"},
        {"id": 5, "category": "Sales", "urgency": "High", "summary": "Inquiry about enterprise plan", "email": "charlie.d@example.com"},
    ]
    return {"inquiries": initial_inquiries}
