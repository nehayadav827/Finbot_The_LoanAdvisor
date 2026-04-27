"""
Verification Agent – collects and validates KYC details.
"""
from services.groq_service import extract_json
from services.crm_service import lookup_customer, verify_pan

VERIFY_SYSTEM = """You are a KYC verification assistant for FinBot NBFC.
Your job is to politely collect:
- phone (10-digit Indian mobile number)
- pan (PAN card: format ABCDE1234F)

Rules:
1. Ask for phone first, then PAN.
2. Validate format before accepting: phone must be 10 digits, PAN must match [A-Z]{5}[0-9]{4}[A-Z].
3. If format is wrong, politely point out the correct format and ask again.
4. Keep tone warm and reassuring about data security.
5. Respond ONLY in JSON with keys: reply, phone, pan, ready_to_verify.
6. Set ready_to_verify=true only when both phone and pan are present and format-valid.
7. Set null for fields not yet collected."""

async def run_verification_agent(session: dict, user_message: str) -> dict:
    customer = session["customer"]
    history = session["history"][-6:]

    context = f"""
Already collected:
- phone: {customer.get('phone')}
- pan: {customer.get('pan')}
"""
    messages = []
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_message + "\n\n[CONTEXT]" + context})

    result = await extract_json(VERIFY_SYSTEM, messages)

    if result.get("phone"):
        session["customer"]["phone"] = result["phone"]
    if result.get("pan"):
        session["customer"]["pan"] = result["pan"]

    if result.get("ready_to_verify"):
        phone = session["customer"]["phone"]
        pan = session["customer"]["pan"]

        crm_record = lookup_customer(phone)
        if not crm_record:
            session["customer"]["kyc_verified"] = False
            return {
                "reply": "I couldn't find your details in our records. Please check your phone number and try again.",
                "verified": False,
                "crm_record": None,
            }

        pan_ok = verify_pan(phone, pan)
        if not pan_ok:
            session["customer"]["kyc_verified"] = False
            return {
                "reply": "The PAN you entered doesn't match our records. Please double-check and re-enter.",
                "verified": False,
                "crm_record": None,
            }

        # All good – populate session with CRM data
        session["customer"]["name"] = crm_record["name"]
        session["customer"]["dob"] = crm_record["dob"]
        session["customer"]["credit_score"] = crm_record["credit_score"]
        session["customer"]["income"] = crm_record["monthly_income"]
        session["customer"]["salary_slip_verified"] = crm_record["valid_salary_slip"]
        session["customer"]["kyc_verified"] = True
        session["loan"]["_pre_approved_limit"] = crm_record["pre_approved_limit"]

        return {
            "reply": (
                f"Great news, {crm_record['name']}! ✅ Your KYC details have been verified successfully. "
                "Let me now assess your loan eligibility..."
            ),
            "verified": True,
            "crm_record": crm_record,
        }

    return {
        "reply": result.get("reply", "Could you please share your phone number to proceed?"),
        "verified": False,
        "crm_record": None,
    }
