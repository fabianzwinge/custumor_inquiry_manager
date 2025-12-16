from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from typing import Literal

class InquiryClassification(BaseModel):
    category: Literal["Technical", "Billing", "Sales", "General", "N/A"]
    urgency: Literal["High", "Medium", "Low", "N/A"]
    summary: str

def get_llm_chain():
    try:
        model = ChatBedrock(
            model_id="mistral.mistral-small-2402-v1:0",
            region_name="us-east-1",
            model_kwargs={"temperature": 0.1},
        )

        parser = JsonOutputParser(pydantic_object=InquiryClassification)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that classifies customer inquiries.\n"
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
        return chain, parser
    except Exception as e:
        print(f"FATAL: Failed to initialize LangChain components on startup: {e}")
        return None, None

chain, parser = get_llm_chain()
