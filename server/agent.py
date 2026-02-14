"""
Apex Financial — AI Agent Module
Powers the checking account chatbot using OpenAI GPT-4o with tool/function calling.
"""
from __future__ import annotations

import os
import re
import json
import random
import string
import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are Apex, the AI banking assistant for Apex Financial. Your job is to help customers open a new checking account.

## Your Personality
- Professional yet friendly and warm
- Concise — keep responses short (1-3 sentences max)
- Use occasional emojis to feel approachable (👋, ✅, 🔒, 🎉) but don't overdo it

## Account Opening Process
You MUST collect the following information, ONE FIELD AT A TIME, in this order:
1. First name
2. Last name
3. Email address
4. Phone number (10 digits)
5. Date of birth (MM/DD/YYYY format, must be 18+)
6. Social Security Number (9 digits — reassure the user it's encrypted and secure)
7. Street address
8. City
9. State (2-letter US state code)
10. ZIP code (5 digits)

## Rules
- Ask for ONE piece of information at a time. Never ask for multiple fields in a single message.
- After the user provides a value, ALWAYS call the validate_field tool to check it before moving on.
- If validation fails, tell the user the error and ask them to re-enter that field.
- If validation succeeds, acknowledge briefly and ask for the next field.
- After ALL 10 fields are collected and validated, present a summary of the information and ask the user to confirm it's correct.
- If the user wants to edit, ask which field they'd like to change and re-collect just that field.
- Once confirmed, call show_agreement to retrieve the Terms & Conditions.
- Present a BRIEF summary of the key terms (fees, FDIC insurance, privacy) and ask the user to type "I agree" to accept.
- Only after the user explicitly agrees (says "I agree", "yes I agree", "agree", etc.), call create_account with all the collected data.
- If the user declines, respect their decision and let them know they can come back anytime.
- NEVER fabricate or assume data. ALWAYS use the values the user provides.
- If the user asks unrelated questions, politely redirect them back to the account opening process.
- When presenting the review summary, mask the SSN showing only the last 4 digits (e.g., ***-**-6789).

## Important
- You are ONLY able to help with opening checking accounts. For other products (credit cards, savings), let the user know those services are coming soon.
- Always maintain context of what has already been collected so you don't re-ask for information.
"""

# ---------------------------------------------------------------------------
# Tool Definitions (for OpenAI function calling)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "validate_field",
            "description": "Validate a single form field value for the checking account application. Call this every time the user provides a value for a field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_name": {
                        "type": "string",
                        "enum": ["firstName", "lastName", "email", "phone", "dateOfBirth", "ssn", "street", "city", "state", "zip"],
                        "description": "The name of the field to validate"
                    },
                    "value": {
                        "type": "string",
                        "description": "The value provided by the user"
                    }
                },
                "required": ["field_name", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_agreement",
            "description": "Retrieve the Terms & Conditions document. Call this after all fields are collected and confirmed by the user, before account creation.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_account",
            "description": "Create the checking account after the user has agreed to the Terms & Conditions. Pass all validated customer data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string", "description": "10-digit phone number"},
                    "dateOfBirth": {"type": "string", "description": "Date in MM/DD/YYYY or YYYY-MM-DD format"},
                    "ssn": {"type": "string", "description": "9-digit SSN"},
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string", "description": "2-letter US state code"},
                    "zip": {"type": "string", "description": "5-digit ZIP code"}
                },
                "required": ["firstName", "lastName", "email", "phone", "dateOfBirth", "ssn", "street", "city", "state", "zip"]
            }
        }
    }
]

# ---------------------------------------------------------------------------
# Validation Logic
# ---------------------------------------------------------------------------

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC",
}


def validate_field(field_name: str, value: str) -> dict:
    """Validate a single field. Returns {valid: bool, message: str, cleaned_value: str}."""
    v = value.strip()

    if field_name == "firstName" or field_name == "lastName":
        label = "First name" if field_name == "firstName" else "Last name"
        if not v:
            return {"valid": False, "message": f"{label} is required."}
        if len(v) < 2 or len(v) > 50:
            return {"valid": False, "message": f"{label} must be 2–50 characters."}
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            return {"valid": False, "message": f"{label} can only contain letters, spaces, hyphens, and apostrophes."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "email":
        if not v:
            return {"valid": False, "message": "Email is required."}
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
            return {"valid": False, "message": "Please enter a valid email address."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "phone":
        digits = re.sub(r"\D", "", v)
        if len(digits) != 10:
            return {"valid": False, "message": "Phone number must be exactly 10 digits."}
        return {"valid": True, "message": "Valid", "cleaned_value": digits}

    elif field_name == "dateOfBirth":
        if not v:
            return {"valid": False, "message": "Date of birth is required."}
        dob = None
        if re.match(r"^\d{2}/\d{2}/\d{4}$", v):
            try:
                dob = datetime.strptime(v, "%m/%d/%Y").date()
            except ValueError:
                return {"valid": False, "message": "Invalid date. Use MM/DD/YYYY format."}
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            try:
                dob = datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                return {"valid": False, "message": "Invalid date. Use YYYY-MM-DD format."}
        else:
            return {"valid": False, "message": "Please enter date in MM/DD/YYYY format."}
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            return {"valid": False, "message": "You must be at least 18 years old."}
        if age > 120:
            return {"valid": False, "message": "Please enter a valid date of birth."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "ssn":
        digits = re.sub(r"\D", "", v)
        if len(digits) != 9:
            return {"valid": False, "message": "SSN must be exactly 9 digits."}
        if digits.startswith("000") or digits.startswith("666") or digits.startswith("9"):
            return {"valid": False, "message": "Please enter a valid SSN."}
        return {"valid": True, "message": "Valid", "cleaned_value": digits}

    elif field_name == "street":
        if len(v) < 5 or len(v) > 100:
            return {"valid": False, "message": "Street address must be 5–100 characters."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "city":
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            return {"valid": False, "message": "City can only contain letters and spaces."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "state":
        v = v.upper()
        if v not in VALID_STATES:
            return {"valid": False, "message": "Please enter a valid 2-letter US state code (e.g., CA, NY, TX)."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    elif field_name == "zip":
        if not re.match(r"^\d{5}$", v):
            return {"valid": False, "message": "ZIP code must be exactly 5 digits."}
        return {"valid": True, "message": "Valid", "cleaned_value": v}

    return {"valid": False, "message": f"Unknown field: {field_name}"}


# ---------------------------------------------------------------------------
# Agreement Text
# ---------------------------------------------------------------------------

TERMS_AND_CONDITIONS = """
APEX FINANCIAL — CHECKING ACCOUNT TERMS & CONDITIONS
Effective Date: January 1, 2026

1. ACCOUNT AGREEMENT — By opening a checking account with Apex Financial, you agree to these terms.
2. ELIGIBILITY — Must be 18+ and a legal U.S. resident.
3. ACCOUNT OWNERSHIP — Account held in name(s) provided during application.
4. DEPOSITS & WITHDRAWALS — Via direct deposit, mobile check deposit, wire transfer, debit card, ATM, or check.
5. FEES — Monthly Maintenance: $0 | ATM (non-network): $0 | Overdraft: $0 | Domestic Wire: $15 | International Wire: $30
6. ELECTRONIC COMMUNICATIONS — You consent to receive statements and notices electronically.
7. PRIVACY — Your personal information (including SSN) is securely stored and never sold to third parties.
8. FDIC INSURANCE — Deposits insured up to $250,000 per depositor.
9. ACCOUNT CLOSURE — You may close at any time; Bank may close with 30 days notice.
10. GOVERNING LAW — Governed by Delaware state and federal law.
11. DISPUTE RESOLUTION — Binding arbitration via American Arbitration Association.
"""


def show_agreement() -> dict:
    """Return the Terms & Conditions text."""
    return {
        "terms": TERMS_AND_CONDITIONS.strip(),
        "instruction": "Present these terms to the user and ask them to type 'I agree' to accept."
    }


def create_account(data: dict) -> dict:
    """Create a checking account with validated data. Returns account/routing numbers."""
    account_number = "".join(random.choices(string.digits, k=10))
    routing_number = "".join(random.choices(string.digits, k=9))
    return {
        "success": True,
        "accountNumber": account_number,
        "routingNumber": routing_number,
        "accountType": "Checking",
        "customerName": f"{data.get('firstName', '')} {data.get('lastName', '')}",
        "message": "Account created successfully!"
    }


# ---------------------------------------------------------------------------
# Tool Execution
# ---------------------------------------------------------------------------

def execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute a tool call and return the result as a JSON string."""
    if tool_name == "validate_field":
        result = validate_field(arguments["field_name"], arguments["value"])
    elif tool_name == "show_agreement":
        result = show_agreement()
    elif tool_name == "create_account":
        result = create_account(arguments)
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result)


# ---------------------------------------------------------------------------
# Session Management
# ---------------------------------------------------------------------------

# In-memory session store: session_id -> list of messages
sessions: dict[str, list[dict]] = {}


def get_or_create_session(session_id: str | None) -> tuple[str, list[dict]]:
    """Get existing session or create a new one with the system prompt."""
    if not session_id or session_id not in sessions:
        session_id = session_id or str(uuid.uuid4())
        sessions[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return session_id, sessions[session_id]


# ---------------------------------------------------------------------------
# Agent Loop
# ---------------------------------------------------------------------------

async def process_message(session_id: str | None, user_message: str) -> dict:
    """
    Process a user message through the AI agent.
    Handles the agentic loop: send to LLM → execute tool calls → repeat until text response.
    Returns {session_id, reply, metadata}.
    """
    session_id, history = get_or_create_session(session_id)

    # Add user message to history
    history.append({"role": "user", "content": user_message})

    metadata = {}

    # Agentic loop — keep going while the model wants to call tools
    max_iterations = 10  # safety limit
    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1024,
        )

        assistant_message = response.choices[0].message

        # If the model wants to call tools
        if assistant_message.tool_calls:
            # Add the assistant message with tool calls to history
            history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                tool_result = execute_tool(fn_name, fn_args)

                # Check if this is a successful account creation
                if fn_name == "create_account":
                    result_data = json.loads(tool_result)
                    if result_data.get("success"):
                        metadata["accountCreated"] = True
                        metadata["accountNumber"] = result_data["accountNumber"]
                        metadata["routingNumber"] = result_data["routingNumber"]
                        metadata["accountType"] = result_data["accountType"]

                # Add tool result to history
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

            # Continue the loop to get the model's next response
            continue

        # No tool calls — we have a final text response
        reply = assistant_message.content or ""
        history.append({"role": "assistant", "content": reply})

        return {
            "sessionId": session_id,
            "reply": reply,
            "metadata": metadata,
        }

    # Fallback if we hit max iterations
    fallback = "I'm sorry, I encountered an issue processing your request. Please try again."
    history.append({"role": "assistant", "content": fallback})
    return {
        "sessionId": session_id,
        "reply": fallback,
        "metadata": metadata,
    }
