"""
Generates a PDF sanction letter and saves it to /tmp/sanctions/.
Returns the file path.
"""
import os
import uuid
from datetime import date

OUTPUT_DIR = "/tmp/finbot_sanctions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_sanction_letter(session: dict) -> str:
    """
    Generate a plain-text sanction letter and save as .txt (acts as PDF placeholder).
    In production swap fpdf2 or reportlab for actual PDF generation.
    Returns file path.
    """
    c = session["customer"]
    l = session["loan"]
    u = session["underwriting"]

    emi = u.get("emi") or 0
    rate = (u.get("interest_rate") or 0.18) * 100
    total = u.get("total_payable") or 0
    today = date.today().strftime("%d %B %Y")

    letter = f"""
================================================================================
                         FINBOT LENDING SOLUTIONS
                         LOAN SANCTION LETTER
================================================================================

Date: {today}
Reference No: FNBT-{uuid.uuid4().hex[:8].upper()}

To,
{c.get('name', 'Valued Customer')}
Phone: {c.get('phone', 'N/A')}
PAN: {c.get('pan', 'N/A')}

Dear {c.get('name', 'Applicant')},

We are pleased to inform you that your personal loan application has been
SANCTIONED subject to the terms and conditions mentioned below.

────────────────────────────────────────────────────────────────────────────────
                          LOAN SANCTION DETAILS
────────────────────────────────────────────────────────────────────────────────

  Loan Amount Sanctioned   : ₹{float(l.get('amount') or 0):,.2f}
  Loan Purpose             : {l.get('purpose') or 'Personal Use'}
  Tenure                   : {l.get('tenure') or 'N/A'} months
  Rate of Interest (p.a.)  : {rate:.2f}% (Reducing Balance)
  Monthly EMI              : ₹{float(emi):,.2f}
  Total Amount Payable     : ₹{float(total):,.2f}

────────────────────────────────────────────────────────────────────────────────
                          TERMS & CONDITIONS
────────────────────────────────────────────────────────────────────────────────

1. The loan is subject to execution of the Loan Agreement before disbursement.
2. The EMI will be debited via NACH/ECS mandate on the due date each month.
3. Prepayment charges: 2% on outstanding principal after 6 months.
4. This sanction is valid for 30 days from the date of this letter.
5. Disbursement subject to satisfactory completion of all KYC requirements.
6. Any misrepresentation will result in immediate cancellation.

────────────────────────────────────────────────────────────────────────────────

This sanction letter is issued based on information provided by you and is
subject to change if any material information is found to be incorrect.

For queries, contact: support@finbot.in | 1800-XXX-XXXX

Yours sincerely,

[Authorised Signatory]
FinBot Lending Solutions Pvt. Ltd.
NBFC Registration No: N-14.03XXX

================================================================================
                    ** COMPUTER GENERATED LETTER **
================================================================================
"""

    filename = f"sanction_{uuid.uuid4().hex[:10]}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(letter)

    return filepath


def get_download_url(filepath: str) -> str:
    """Return a pseudo URL for the sanction file."""
    filename = os.path.basename(filepath)
    return f"/download/sanction/{filename}"