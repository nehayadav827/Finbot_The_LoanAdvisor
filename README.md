# 🤖 FinBot — AI-Powered Loan Sales Assistant

> An Agentic AI system for NBFCs that automates the end-to-end personal loan journey — from customer intent to sanction letter generation — using **Groq LLM**, **FastAPI**, and **React**.

---

**Live link** : https://fin-bot-azure.vercel.app/

---
## 📐 Architecture Overview

```
User (React Chat UI)
        │
        ▼
  FastAPI Backend
        │
   Master Agent  ◄── Groq LLaMA 3.3 70B (intent, conversation)
        │
   ┌────┴──────────────────────────┐
   │           Worker Agents       │
   ├─ Sales Agent                  │  ← Loan term extraction & negotiation
   ├─ Verification Agent           │  ← KYC via Mock CRM
   ├─ Underwriting Agent           │  ← Deterministic Rules Engine
   └─ Sanction Agent               │  ← PDF sanction letter generator
        │
   Backend Services
   ├─ Mock CRM (JSON)              ← KYC / PAN / credit score
   ├─ Underwriting Rules Engine    ← 6-rule deterministic engine
   └─ Sanction Service             ← Letter generation
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **Backend** | Python 3.11+, FastAPI (ASGI), Uvicorn |
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Session Storage** | In-memory (replace with Redis/Postgres for prod) |
| **Decision Logic** | Hybrid: Groq for NLU + deterministic rules engine |
| **Document Gen** | Plain text (swap in `fpdf2`/`reportlab` for real PDF) |

---

## 🔍 Underwriting Rules Engine

The rules engine is **fully deterministic and auditable** — Groq is **never** used for financial decisions. Rules run in sequence; the first failure causes rejection.

| # | Rule | Threshold |
|---|---|---|
| 1 | Loan bounds | ₹10,000 – ₹20,00,000 |
| 2 | Tenure bounds | 6 – 60 months |
| 3 | Minimum credit score | ≥ 700 |
| 4 | Pre-approved limit check | Loan ≤ limit → approve; limit < loan ≤ 2× limit → need salary slip; > 2× limit → reject |
| 5 | Loan-to-income ratio | ≤ 36× monthly income |
| 6 | EMI affordability | EMI ≤ 40% of monthly income |

EMI is computed using the standard **reducing-balance formula**:
```
EMI = P × r × (1+r)^n / ((1+r)^n − 1)
```
where `r = annual_rate / 12`, `n = tenure_months`.

---

## 🧩 Agent Roles

### Master Agent
- Owns the full conversation state machine
- Stages: `greeting → sales → verification → underwriting → approved/rejected`
- Orchestrates worker agents; makes no financial decisions itself

### Sales Agent (Groq-powered)
- Extracts `loan_amount`, `tenure_months`, `purpose`, `monthly_income` from free-text
- Handles "2 lakh" → 200000 conversion, years → months, etc.
- Returns structured JSON; Master Agent writes to session DB

### Verification Agent (Groq + CRM lookup)
- Collects and format-validates `phone` (10 digits) and `PAN` (`ABCDE1234F` pattern)
- Looks up customer in Mock CRM; cross-validates PAN
- Populates credit score, income, pre-approved limit into session

### Underwriting Agent (Rules Engine)
- Reads session data, calls `rules/underwriting_rules.py`
- Rules engine returns structured `UnderwritingResult`
- Groq only used to humanize the explanation text (no decision power)

### Sanction Agent
- Generates a formatted sanction letter with all loan terms
- Stores file in `/tmp/finbot_sanctions/`
- Returns a download URL

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API Key](https://console.groq.com) (free tier available)

---

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set: GROQ_API_KEY=your_key_here

# Run the server
uvicorn main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

---

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🧪 Demo Accounts

Use these phone + PAN combinations during KYC verification:

| Phone | PAN | Credit Score | Income | Result |
|---|---|---|---|---|
| `9876543210` | `ABCDE1234F` | 750 | ₹60,000 | ✅ Likely approved |
| `9123456780` | `FGHIJ5678K` | 680 | ₹35,000 | ❌ Low credit score |
| `9988776655` | `LMNOP9012Q` | 610 | ₹25,000 | ❌ Low credit + invalid slip |
| `8000000001` | `RSTUV3456W` | 720 | ₹45,000 | ✅ Likely approved |

---

## 💬 Sample Conversation Flow

```
User:  I need a home renovation loan
Bot:   Great! How much would you like to borrow and for how long?

User:  2 lakh for 24 months, my salary is 50000
Bot:   Got it — ₹2,00,000 over 24 months. 
       To verify your identity, please share your mobile number.

User:  9876543210
Bot:   And your PAN card number?

User:  ABCDE1234F
Bot:   ✅ KYC verified, Rahul Sharma!
       📋 Underwriting: Congratulations! Your loan of ₹2,00,000 has been approved.
       Monthly EMI: ₹9,982 at 18% p.a.
       🎉 [Download Sanction Letter]
```

---

## 📁 Project Structure

```
finbot/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── agents/
│   │   ├── master_agent.py        # State machine + orchestrator
│   │   ├── sales_agent.py         # Loan term extraction
│   │   ├── verification_agent.py  # KYC validation
│   │   └── underwriting_agent.py  # Rules engine wrapper
│   ├── rules/
│   │   └── underwriting_rules.py  # 6-rule deterministic engine
│   └── services/
│       ├── groq_service.py        # Groq API client
│       ├── crm_service.py         # Mock CRM / KYC database
│       ├── session_store.py       # In-memory session state
│       └── sanction_service.py    # Sanction letter generator
│
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx                # Root component + layout
        ├── index.css              # Global styles + animations
        ├── main.jsx
        ├── hooks/
        │   └── useChat.js         # Conversation state management
        ├── utils/
        │   └── api.js             # Axios API client
        └── components/
            ├── Header.jsx
            ├── StageBar.jsx       # Progress indicator
            ├── MessageBubble.jsx  # Chat messages
            ├── TypingIndicator.jsx
            ├── QuickReplies.jsx   # Suggestion chips
            ├── ChatInput.jsx      # Text input bar
            ├── LoanPanel.jsx      # Sidebar loan summary
            └── WelcomeScreen.jsx  # Initial landing view
```

---

## 🔧 Configuration

All underwriting thresholds are in `backend/rules/underwriting_rules.py`:

```python
MIN_CREDIT_SCORE          = 700
MAX_LOAN_TO_INCOME_RATIO  = 36
MAX_EMI_TO_INCOME_RATIO   = 0.40
MAX_LOAN_ABSOLUTE         = 2_000_000
MIN_LOAN_ABSOLUTE         = 10_000
MAX_TENURE_MONTHS         = 60
ANNUAL_INTEREST_RATE      = 0.18
OVER_LIMIT_MULTIPLIER     = 2.0
```

---

## 🛣 Future Scope

- [ ] Replace Mock CRM with real KYC / PAN / bureau APIs
- [ ] Swap in `fpdf2` for proper PDF sanction letters
- [ ] Redis session store for horizontal scaling
- [ ] WhatsApp / SMS channel via Twilio
- [ ] Fraud & AML detection agents
- [ ] Multilingual support (Hindi, Tamil, etc.)
- [ ] Cross-sell agents (credit cards, insurance, BNPL)
- [ ] Firebase Auth for user identity management

---

## 📄 License

MIT — built for the IIIT Guwahati FinTech AI project.
