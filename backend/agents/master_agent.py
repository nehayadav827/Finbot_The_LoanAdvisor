"""
Master Agent – owns the conversation state machine and orchestrates worker agents.
Stages: greeting → sales → verification → underwriting → approved/rejected
"""
from services.groq_service import call_groq
from agents.sales_agent import run_sales_agent
from agents.verification_agent import run_verification_agent
from agents.underwriting_agent import run_underwriting_agent
from services.sanction_service import generate_sanction_letter, get_download_url

GREETING_SYSTEM = """You are FinBot, a friendly AI loan assistant for an NBFC.
Greet the customer warmly. Ask what kind of loan they're looking for.
Keep it to 2 sentences max. Do NOT mention specific amounts yet."""

class MasterAgent:
    def __init__(self, session: dict, session_store):
        self.session = session
        self.session_store = session_store

    async def process(self, user_message: str) -> dict:
        stage = self.session["stage"]
        
        # Append user message to history
        self.session["history"].append({"role": "user", "content": user_message})

        result = await self._dispatch(stage, user_message)

        # Append assistant reply to history
        self.session["history"].append({"role": "assistant", "content": result["reply"]})

        return {
            "reply": result["reply"],
            "stage": self.session["stage"],
            "loan_data": self._loan_summary(),
            "sanction_url": self.session.get("sanction_url"),
        }

    async def _dispatch(self, stage: str, message: str) -> dict:
        if stage == "greeting":
            return await self._handle_greeting(message)
        elif stage == "sales":
            return await self._handle_sales(message)
        elif stage == "verification":
            return await self._handle_verification(message)
        elif stage == "underwriting":
            return await self._handle_underwriting()
        elif stage in ("approved", "rejected"):
            return {"reply": "Your application has already been processed. Start a new chat to apply again."}
        else:
            return await self._handle_greeting(message)

    async def _handle_greeting(self, message: str) -> dict:
        # Check if message contains loan intent
        loan_keywords = ["loan", "borrow", "lakh", "amount", "emi", "credit", "finance", "money"]
        has_intent = any(kw in message.lower() for kw in loan_keywords)

        if has_intent:
            self.session["stage"] = "sales"
            return await self._handle_sales(message)

        reply = await call_groq(
            GREETING_SYSTEM,
            [{"role": "user", "content": message}],
            temperature=0.5,
            max_tokens=100,
        )
        self.session["stage"] = "sales"
        return {"reply": reply.strip()}

    async def _handle_sales(self, message: str) -> dict:
        result = await run_sales_agent(self.session, message)
        if result["complete"]:
            self.session["stage"] = "verification"
            transition = (
                f"{result['reply']} "
                "Now, to verify your identity, could you please share your registered mobile number?"
            )
            return {"reply": transition}
        return {"reply": result["reply"]}

    async def _handle_verification(self, message: str) -> dict:
        result = await run_verification_agent(self.session, message)
        if result["verified"]:
            self.session["stage"] = "underwriting"
            # Immediately run underwriting
            uw = await run_underwriting_agent(self.session)
            if uw["approved"]:
                self.session["stage"] = "approved"
                # Generate sanction letter
                filepath = generate_sanction_letter(self.session)
                url = get_download_url(filepath)
                self.session["sanction_url"] = url
                full_reply = (
                    f"{result['reply']}\n\n"
                    f"📋 **Underwriting Result:** {uw['reply']}\n\n"
                    f"🎉 Your sanction letter is ready! [Download Sanction Letter]({url})"
                )
            else:
                self.session["stage"] = "rejected"
                full_reply = (
                    f"{result['reply']}\n\n"
                    f"⚠️ **Underwriting Result:** {uw['reply']}"
                )
            return {"reply": full_reply}
        return {"reply": result["reply"]}

    async def _handle_underwriting(self) -> dict:
        # Should not reach here directly (called from verification)
        uw = await run_underwriting_agent(self.session)
        if uw["approved"]:
            self.session["stage"] = "approved"
        else:
            self.session["stage"] = "rejected"
        return {"reply": uw["reply"]}

    def _loan_summary(self) -> dict:
        l = self.session["loan"]
        c = self.session["customer"]
        u = self.session["underwriting"]
        return {
            "amount": l.get("amount"),
            "tenure": l.get("tenure"),
            "purpose": l.get("purpose"),
            "emi": l.get("emi"),
            "customer_name": c.get("name"),
            "credit_score": c.get("credit_score"),
            "decision": u.get("decision"),
            "interest_rate": u.get("interest_rate"),
        }
