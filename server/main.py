"""
Apex Financial — Checking Account API
FastAPI backend for processing account creation requests.
Includes AI agent chat endpoint powered by OpenAI GPT-4o.
"""

import re
import random
import string
from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from agent import process_message

app = FastAPI(title="Apex Financial API", version="2.0.0")

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- Chat Models -----

class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None

class ChatResponse(BaseModel):
    sessionId: str
    reply: str
    metadata: dict = {}


# ----- Account Models -----

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str

    @field_validator("street")
    @classmethod
    def validate_street(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5 or len(v) > 100:
            raise ValueError("Street address must be 5–100 characters.")
        return v

    @field_validator("city")
    @classmethod
    def validate_city(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("City can only contain letters and spaces.")
        return v

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        valid_states = {
            "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
            "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
            "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
            "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
            "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC",
        }
        v = v.strip().upper()
        if v not in valid_states:
            raise ValueError("Please provide a valid 2-letter US state code.")
        return v

    @field_validator("zip")
    @classmethod
    def validate_zip(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^\d{5}$", v):
            raise ValueError("ZIP code must be exactly 5 digits.")
        return v


class AccountRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    dateOfBirth: str
    ssn: str
    address: Address
    agreedToTerms: bool

    @field_validator("firstName")
    @classmethod
    def validate_first_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 50:
            raise ValueError("First name must be 2–50 characters.")
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("First name can only contain letters, spaces, hyphens, and apostrophes.")
        return v

    @field_validator("lastName")
    @classmethod
    def validate_last_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 50:
            raise ValueError("Last name must be 2–50 characters.")
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Last name can only contain letters, spaces, hyphens, and apostrophes.")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
            raise ValueError("Please provide a valid email address.")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return digits

    @field_validator("dateOfBirth")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        v = v.strip()
        dob = None
        if re.match(r"^\d{2}/\d{2}/\d{4}$", v):
            try:
                dob = datetime.strptime(v, "%m/%d/%Y").date()
            except ValueError:
                raise ValueError("Please provide a valid date (MM/DD/YYYY).")
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            try:
                dob = datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Please provide a valid date (YYYY-MM-DD).")
        else:
            raise ValueError("Date of birth must be in MM/DD/YYYY or YYYY-MM-DD format.")

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValueError("You must be at least 18 years old to open an account.")
        if age > 120:
            raise ValueError("Please provide a valid date of birth.")
        return v

    @field_validator("ssn")
    @classmethod
    def validate_ssn(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 9:
            raise ValueError("SSN must be exactly 9 digits.")
        if digits.startswith("000") or digits.startswith("666") or digits.startswith("9"):
            raise ValueError("Please provide a valid SSN.")
        return digits

    @field_validator("agreedToTerms")
    @classmethod
    def validate_agreed(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must agree to the Terms & Conditions to open an account.")
        return v


class AccountResponse(BaseModel):
    accountNumber: str
    routingNumber: str
    accountType: str
    message: str
    customerName: str


# ----- Endpoints -----

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Apex Financial API", "version": "2.0.0"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    AI Agent chat endpoint.
    Sends user message through the GPT-4o agent with tool calling.
    """
    try:
        result = await process_message(request.sessionId, request.message)
        return ChatResponse(
            sessionId=result["sessionId"],
            reply=result["reply"],
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/api/accounts", response_model=AccountResponse)
async def create_account(request: AccountRequest):
    """
    Create a new checking account (direct API).
    Validates all input data and returns account + routing numbers.
    """
    account_number = "".join(random.choices(string.digits, k=10))
    routing_number = "".join(random.choices(string.digits, k=9))

    return AccountResponse(
        accountNumber=account_number,
        routingNumber=routing_number,
        accountType="Checking",
        message="Account created successfully!",
        customerName=f"{request.firstName} {request.lastName}",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
