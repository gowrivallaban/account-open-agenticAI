# Apex Financial — Agentic AI Chatbot for Checking Account Opening

A full-stack banking application with an **AI-powered chatbot** (OpenAI GPT-4o with tool calling) that guides users through opening a checking account. Built with **React (Vite)** and **Python FastAPI**.

---

## Features

### Landing Page
- Dark glass-morphism design with teal/gold accents and micro-animations
- Three product cards: **Credit Cards**, **Checking Account**, **Savings Account**
- Hero section with CTA to launch the chatbot

### AI Chatbot (GPT-4o Agent with Tool Calling)
The chatbot is powered by a **real AI agent** running on the backend. The agent uses OpenAI GPT-4o with function calling to:
1. **Collect information** — Asks for each field naturally, one at a time
2. **Validate in real-time** — Calls `validate_field` tool for each user input
3. **Present Terms & Conditions** — Calls `show_agreement` tool and asks for consent
4. **Create the account** — Calls `create_account` tool after user agrees, returning account & routing numbers

The AI handles the conversation naturally — it can answer follow-up questions, handle corrections, and guide the user through the entire flow.

### Backend (Python FastAPI + OpenAI)
- `POST /api/chat` — AI agent chat endpoint (GPT-4o with tool calling)
- `POST /api/accounts` — Direct account creation API with Pydantic validation
- `GET /api/health` — Health check endpoint
- In-memory session management for conversation context

---

## Getting Started

### Prerequisites
- **Node.js** (v18+)
- **Python 3.9+**
- **OpenAI API Key** ([get one here](https://platform.openai.com/api-keys))

### Installation & Running

```bash
# 1. Clone the repo
git clone <repo-url>
cd account-open-agenticAI

# 2. Set your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > server/.env

# 3. Start the backend (terminal 1)
cd server
pip3 install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000

# 4. Start the frontend (terminal 2)
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Project Structure

```
account-open-agenticAI/
├── index.html                  # HTML entry point
├── package.json                # Frontend dependencies
├── vite.config.js              # Vite config with API proxy to port 8000
├── server/
│   ├── main.py                 # FastAPI endpoints (/api/chat, /api/accounts)
│   ├── agent.py                # AI agent (GPT-4o + tool calling)
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # OpenAI API key (not committed)
└── src/
    ├── main.jsx                # React entry point
    ├── App.jsx                 # Root component
    ├── index.css               # Design system (dark theme, glass-morphism)
    ├── components/
    │   ├── LandingPage.jsx     # Banking products landing page
    │   ├── ChatbotWidget.jsx   # Floating chatbot panel with FAB button
    │   ├── ChatFlow.jsx        # Chat relay to backend AI agent
    │   └── Agreement.jsx       # Terms & Conditions (legacy, kept for reference)
    └── utils/
        └── validators.js       # Frontend validators (legacy, kept for reference)
```

---

## Walkthrough

### 1. Landing Page
The landing page showcases three banking products. The **Checking Account** card and the floating chat bubble (💬) both launch the AI assistant.

### 2. AI-Powered Conversation
The chatbot is powered by GPT-4o. It naturally guides the user through each required field, validates inputs using tool calling, and handles corrections conversationally.

### 3. Terms & Conditions
After collecting all data, the AI agent presents the terms and asks the user to type "I agree" to provide consent.

### 4. Account Creation
Once the user agrees, the agent calls the `create_account` tool and displays:
- **Account Number** (10 digits)
- **Routing Number** (9 digits)
- **Account Type** (Checking)

---

## API Reference

### `POST /api/accounts`

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john.smith@example.com",
  "phone": "5551234567",
  "dateOfBirth": "01/15/1990",
  "ssn": "123456789",
  "address": {
    "street": "123 Main Street",
    "city": "Austin",
    "state": "TX",
    "zip": "78701"
  },
  "agreedToTerms": true
}
```

**Success Response (200):**
```json
{
  "accountNumber": "2952319417",
  "routingNumber": "584053880",
  "accountType": "Checking",
  "message": "Account created successfully!",
  "customerName": "John Smith"
}
```

**Validation Error (422):** Pydantic validation errors with field-level detail.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 6 |
| Styling | Vanilla CSS (glass-morphism, dark theme) |
| Backend | Python FastAPI, Pydantic |
| Font | Inter (Google Fonts) |

---

## License

© 2026 Apex Financial. All rights reserved.
