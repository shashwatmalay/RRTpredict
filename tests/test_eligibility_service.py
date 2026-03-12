from app.schemas import LoanCheckRequest
from app.services.eligibility_service import evaluate_loan_eligibility


def test_eligibility_passes_for_valid_payload():
    payload = LoanCheckRequest(
        age=30,
        monthly_income=50000,
        credit_score=720,
        loan_amount=200000,
        employment_status="Full-time",
        existing_loans=1,
    )

    eligible, _ = evaluate_loan_eligibility(payload)
    assert eligible is True


def test_eligibility_fails_for_low_credit_score():
    payload = LoanCheckRequest(
        age=30,
        monthly_income=50000,
        credit_score=500,
        loan_amount=200000,
        employment_status="Full-time",
        existing_loans=1,
    )

    eligible, _ = evaluate_loan_eligibility(payload)
    assert eligible is False
