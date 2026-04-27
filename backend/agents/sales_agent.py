"""
Sales Agent – extracts loan intent and negotiates terms.
"""
from services.groq_service import extract_json, call_groq

SALES_SYSTEM = """You are a friendly loan sales assistant for an NBFC called FinBot.
Your job is to understand what the customer wants and collect:
- loan_amount (number in INR, e.g. 200000 for 2 lakhs)
- tenure_months (integer, between 6 and 60)
- purpose (string, e.g. "home renovation", "education", "medical")
- monthly_income (number in INR if mentioned)

Rules:
1. Be conversational and warm, not robotic.
2. If the customer gives an amount in "lakhs" convert to numeric (e.g. "2 lakh" → 200000).
3. If tenure is given in years, convert to months.
4. If something is unclear, ask ONE clarifying question.
5. Once you have all three required fields (amount, tenure, purpose), set complete=true.
6. ALWAYS respond in JSON with keys: reply, loan_amount, tenure_months, purpose, monthly_income, complete.
7. Set null for fields not yet provided.
8. Keep reply under 80 words, friendly tone."""

async def run_sales_agent(session: dict, user_message: str) -> dict:
    """Returns updated loan fields + reply text."""
    history = session["history"][-6:]  # last 6 turns for context
    loan = session["loan"]
    customer = session["customer"]

    context = f"""
Current known data:
- loan_amount: {loan.get('amount')}
- tenure_months: {loan.get('tenure')}
- purpose: {loan.get('purpose')}
- monthly_income: {customer.get('income')}
"""
    messages = []
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_message + "\n\n[CONTEXT]" + context})

    result = await extract_json(SALES_SYSTEM, messages)

    # Update session loan fields with non-null values
    if result.get("loan_amount"):
        session["loan"]["amount"] = float(result["loan_amount"])
    if result.get("tenure_months"):
        session["loan"]["tenure"] = int(result["tenure_months"])
    if result.get("purpose"):
        session["loan"]["purpose"] = result["purpose"]
    if result.get("monthly_income"):
        session["customer"]["income"] = float(result["monthly_income"])

    return {
        "reply": result.get("reply", "Could you tell me more about your loan requirement?"),
        "complete": bool(result.get("complete", False)),
    }
