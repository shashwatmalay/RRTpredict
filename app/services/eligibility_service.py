from app.schemas import LoanCheckRequest


def evaluate_loan_eligibility(payload: LoanCheckRequest) -> tuple[bool, str]:
    income = payload.monthly_income
    score_ok = payload.credit_score > 650
    income_ok = income > 30000
    amount_ok = payload.loan_amount < income * 10
    existing_loans_ok = payload.existing_loans <= 3

    if score_ok and income_ok and amount_ok and existing_loans_ok:
        return True, "User is eligible for the loan"

    return False, "User is not eligible for the loan"
