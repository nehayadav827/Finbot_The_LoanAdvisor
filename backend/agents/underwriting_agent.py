"""
Underwriting Agent – applies the deterministic rules engine and formats result.
"""
from rules.underwriting_rules import evaluate, UnderwritingInput
from services.groq_service import call_groq

EXPLAIN_SYSTEM = """You are a loan officer at FinBot NBFC.
Given an underwriting decision (approved or rejected) with a technical reason, 
write a warm, professional 2–3 sentence explanation for the customer.
If approved: congratulate them, mention EMI and key terms briefly.
If rejected: empathize, clearly state the reason, and (if possible) give one actionable suggestion.
Keep it under 70 words. Do NOT use markdown."""

async def run_underwriting_agent(session: dict) -> dict:
    c = session["customer"]
    l = session["loan"]

    inp = UnderwritingInput(
        loan_amount=float(l.get("amount") or 0),
        tenure_months=int(l.get("tenure") or 12),
        monthly_income=float(c.get("income") or 0),
        credit_score=int(c.get("credit_score") or 0),
        pre_approved_limit=float(l.get("_pre_approved_limit") or 0),
        valid_salary_slip=bool(c.get("salary_slip_verified", False)),
    )

    result = evaluate(inp)

    # Store result in session
    session["underwriting"]["decision"] = "approved" if result.approved else "rejected"
    session["underwriting"]["reason"] = result.reason
    session["underwriting"]["rule_triggered"] = result.rule_triggered
    if result.emi:
        session["underwriting"]["emi"] = result.emi
        session["loan"]["emi"] = result.emi
    if result.total_payable:
        session["underwriting"]["total_payable"] = result.total_payable
    if result.interest_rate:
        session["underwriting"]["interest_rate"] = result.interest_rate

    # Ask Groq to humanize the explanation
    emi_display = f"₹{result.emi:,.2f}" if result.emi else "N/A"
    prompt_msg = f"""
Decision: {"APPROVED" if result.approved else "REJECTED"}
Technical reason: {result.reason}
Loan amount: ₹{inp.loan_amount:,.0f}
Tenure: {inp.tenure_months} months
EMI: {emi_display}
Customer name: {c.get('name', 'the applicant')}
"""
    reply = await call_groq(
        EXPLAIN_SYSTEM,
        [{"role": "user", "content": prompt_msg}],
        temperature=0.4,
        max_tokens=150,
    )

    return {
        "approved": result.approved,
        "reply": reply.strip(),
        "emi": result.emi,
        "rule_triggered": result.rule_triggered,
    }