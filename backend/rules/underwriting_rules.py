"""
FinBot Underwriting Rules Engine
---------------------------------
Rules are deterministic, auditable, and configurable.
Order matters – first failing rule causes rejection.
"""

from dataclasses import dataclass
from typing import Tuple
import math

# ─── Configurable thresholds ─────────────────────────────────────────────────
MIN_CREDIT_SCORE          = 700       # Hard floor
MAX_LOAN_TO_INCOME_RATIO  = 36        # Loan ≤ 36× monthly income
MAX_EMI_TO_INCOME_RATIO   = 0.40      # EMI ≤ 40% net monthly income
MAX_LOAN_ABSOLUTE         = 2_000_000 # ₹20 lakh ceiling
MIN_LOAN_ABSOLUTE         = 10_000    # ₹10k floor
MAX_TENURE_MONTHS         = 60        # 5 years
MIN_TENURE_MONTHS         = 6
ANNUAL_INTEREST_RATE      = 0.18      # 18% p.a. (configurable per product)
OVER_LIMIT_MULTIPLIER     = 2.0       # Can borrow up to 2× pre-approved limit with slip check

# ─── DTOs ────────────────────────────────────────────────────────────────────
@dataclass
class UnderwritingInput:
    loan_amount: float
    tenure_months: int
    monthly_income: float
    credit_score: int
    pre_approved_limit: float
    valid_salary_slip: bool

@dataclass
class UnderwritingResult:
    approved: bool
    reason: str
    emi: float | None = None
    interest_rate: float = ANNUAL_INTEREST_RATE
    total_payable: float | None = None
    rule_triggered: str | None = None

# ─── EMI calculator ──────────────────────────────────────────────────────────
def compute_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """Standard reducing-balance EMI formula."""
    r = annual_rate / 12
    if r == 0:
        return principal / tenure_months
    emi = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    return round(emi, 2)

# ─── Rule evaluators ─────────────────────────────────────────────────────────
def _check_loan_bounds(inp: UnderwritingInput) -> Tuple[bool, str]:
    if inp.loan_amount < MIN_LOAN_ABSOLUTE:
        return False, f"Loan amount ₹{inp.loan_amount:,.0f} is below minimum ₹{MIN_LOAN_ABSOLUTE:,}."
    if inp.loan_amount > MAX_LOAN_ABSOLUTE:
        return False, f"Loan amount ₹{inp.loan_amount:,.0f} exceeds maximum ₹{MAX_LOAN_ABSOLUTE:,}."
    return True, ""

def _check_tenure(inp: UnderwritingInput) -> Tuple[bool, str]:
    if inp.tenure_months < MIN_TENURE_MONTHS:
        return False, f"Tenure {inp.tenure_months} months is below minimum {MIN_TENURE_MONTHS} months."
    if inp.tenure_months > MAX_TENURE_MONTHS:
        return False, f"Tenure {inp.tenure_months} months exceeds maximum {MAX_TENURE_MONTHS} months."
    return True, ""

def _check_credit_score(inp: UnderwritingInput) -> Tuple[bool, str]:
    if inp.credit_score < MIN_CREDIT_SCORE:
        return False, (
            f"Credit score {inp.credit_score} is below the minimum required score of {MIN_CREDIT_SCORE}. "
            "Improving your score may increase future approval chances."
        )
    return True, ""

def _check_pre_approved_limit(inp: UnderwritingInput) -> Tuple[bool, str]:
    """
    Rule:
      - Loan ≤ pre_approved_limit → straight approve (skip salary slip check)
      - pre_approved_limit < Loan ≤ 2× pre_approved_limit → require valid salary slip
      - Loan > 2× pre_approved_limit → reject
    """
    if inp.loan_amount <= inp.pre_approved_limit:
        return True, "within_pre_approved"
    over_limit_ceiling = inp.pre_approved_limit * OVER_LIMIT_MULTIPLIER
    if inp.loan_amount > over_limit_ceiling:
        return False, (
            f"Requested amount ₹{inp.loan_amount:,.0f} exceeds twice your pre-approved limit "
            f"(₹{over_limit_ceiling:,.0f}). Maximum we can offer is ₹{over_limit_ceiling:,.0f}."
        )
    # Between limit and 2× limit – salary slip required
    if not inp.valid_salary_slip:
        return False, (
            f"Loan ₹{inp.loan_amount:,.0f} exceeds your pre-approved limit ₹{inp.pre_approved_limit:,.0f}. "
            "A valid salary slip is required but could not be verified."
        )
    return True, "over_limit_with_slip"

def _check_income_ratio(inp: UnderwritingInput) -> Tuple[bool, str]:
    ratio = inp.loan_amount / inp.monthly_income
    if ratio > MAX_LOAN_TO_INCOME_RATIO:
        max_eligible = inp.monthly_income * MAX_LOAN_TO_INCOME_RATIO
        return False, (
            f"Loan ₹{inp.loan_amount:,.0f} is {ratio:.1f}× your monthly income, "
            f"exceeding the {MAX_LOAN_TO_INCOME_RATIO}× cap. "
            f"Maximum eligible: ₹{max_eligible:,.0f}."
        )
    return True, ""

def _check_emi_affordability(inp: UnderwritingInput, emi: float) -> Tuple[bool, str]:
    ratio = emi / inp.monthly_income
    if ratio > MAX_EMI_TO_INCOME_RATIO:
        return False, (
            f"EMI ₹{emi:,.0f} is {ratio*100:.1f}% of your monthly income ₹{inp.monthly_income:,.0f}, "
            f"exceeding the {int(MAX_EMI_TO_INCOME_RATIO*100)}% affordability limit. "
            f"Consider reducing loan amount or increasing tenure."
        )
    return True, ""

# ─── Main entry point ─────────────────────────────────────────────────────────
def evaluate(inp: UnderwritingInput) -> UnderwritingResult:
    """Run all underwriting rules in sequence. Returns structured decision."""

    # Rule 1 – Loan bounds
    ok, msg = _check_loan_bounds(inp)
    if not ok:
        return UnderwritingResult(approved=False, reason=msg, rule_triggered="LOAN_BOUNDS")

    # Rule 2 – Tenure bounds
    ok, msg = _check_tenure(inp)
    if not ok:
        return UnderwritingResult(approved=False, reason=msg, rule_triggered="TENURE_BOUNDS")

    # Rule 3 – Minimum credit score
    ok, msg = _check_credit_score(inp)
    if not ok:
        return UnderwritingResult(approved=False, reason=msg, rule_triggered="CREDIT_SCORE")

    # Rule 4 – Pre-approved limit check (may require salary slip)
    ok, flag = _check_pre_approved_limit(inp)
    if not ok:
        return UnderwritingResult(approved=False, reason=flag, rule_triggered="PRE_APPROVED_LIMIT")

    # Rule 5 – Income-to-loan ratio
    ok, msg = _check_income_ratio(inp)
    if not ok:
        return UnderwritingResult(approved=False, reason=msg, rule_triggered="INCOME_RATIO")

    # Compute EMI for affordability check
    emi = compute_emi(inp.loan_amount, ANNUAL_INTEREST_RATE, inp.tenure_months)

    # Rule 6 – EMI affordability
    ok, msg = _check_emi_affordability(inp, emi)
    if not ok:
        return UnderwritingResult(approved=False, reason=msg, rule_triggered="EMI_AFFORDABILITY", emi=emi)

    # All rules passed
    total_payable = round(emi * inp.tenure_months, 2)
    return UnderwritingResult(
        approved=True,
        reason="All underwriting criteria met.",
        emi=emi,
        interest_rate=ANNUAL_INTEREST_RATE,
        total_payable=total_payable,
    )
