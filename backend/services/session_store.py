from typing import Optional, Dict
import copy

DEFAULT_SESSION = {
    "stage": "greeting",  # greeting | sales | verification | underwriting | sanction | approved | rejected
    "history": [],        # list of {"role": "user"|"assistant", "content": str}
    "loan": {
        "amount": None,
        "tenure": None,
        "purpose": None,
        "emi": None,
    },
    "customer": {
        "name": None,
        "phone": None,
        "pan": None,
        "dob": None,
        "income": None,
        "salary_slip_verified": False,
        "kyc_verified": False,
        "credit_score": None,
    },
    "underwriting": {
        "decision": None,   # approved | rejected
        "reason": None,
        "max_loan": None,
    },
    "sanction_url": None,
}

class SessionStore:
    def __init__(self):
        self._store: Dict[str, dict] = {}

    def get_or_create(self, session_id: str) -> dict:
        if session_id not in self._store:
            self._store[session_id] = copy.deepcopy(DEFAULT_SESSION)
        return self._store[session_id]

    def get(self, session_id: str) -> Optional[dict]:
        return self._store.get(session_id)

    def save(self, session_id: str, session: dict):
        self._store[session_id] = session

    def delete(self, session_id: str):
        self._store.pop(session_id, None)
