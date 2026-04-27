"""
Mock CRM – simulates KYC database for demo.
In production, replace with real KYC/PAN API calls.
"""

MOCK_CRM = {
    "9876543210": {
        "name": "Rahul Sharma",
        "dob": "1990-05-14",
        "pan": "ABCDE1234F",
        "phone": "9876543210",
        "credit_score": 750,
        "pre_approved_limit": 500000,
        "monthly_income": 60000,
        "employer": "TechCorp Pvt Ltd",
        "valid_salary_slip": True,
    },
    "9123456780": {
        "name": "Priya Mehta",
        "dob": "1995-11-20",
        "pan": "FGHIJ5678K",
        "phone": "9123456780",
        "credit_score": 680,
        "pre_approved_limit": 200000,
        "monthly_income": 35000,
        "employer": "Startup Inc",
        "valid_salary_slip": True,
    },
    "9988776655": {
        "name": "Amit Patel",
        "dob": "1988-03-08",
        "pan": "LMNOP9012Q",
        "phone": "9988776655",
        "credit_score": 610,           # below 700 → reject
        "pre_approved_limit": 100000,
        "monthly_income": 25000,
        "employer": "Self-employed",
        "valid_salary_slip": False,    # invalid slip
    },
    "8000000001": {
        "name": "Sunita Roy",
        "dob": "1993-07-30",
        "pan": "RSTUV3456W",
        "phone": "8000000001",
        "credit_score": 720,
        "pre_approved_limit": 300000,
        "monthly_income": 45000,
        "employer": "Govt School",
        "valid_salary_slip": True,
    },
}

def lookup_customer(phone: str) -> dict | None:
    """Return customer record or None."""
    return MOCK_CRM.get(phone.strip())

def verify_pan(phone: str, pan: str) -> bool:
    """Check PAN matches CRM record."""
    record = MOCK_CRM.get(phone.strip())
    if not record:
        return False
    return record["pan"].upper() == pan.strip().upper()
