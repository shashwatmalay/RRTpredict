from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import LoanApplication, User
from app.schemas import LoanCheckRequest, LoanCheckResponse, LoanHistoryItem
from app.services.eligibility_service import evaluate_loan_eligibility

router = APIRouter(prefix="/loan", tags=["loan"])


@router.post("/check", response_model=LoanCheckResponse)
def check_loan(payload: LoanCheckRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    eligible, message = evaluate_loan_eligibility(payload)

    application = LoanApplication(
        user_id=current_user.id,
        age=payload.age,
        income=payload.monthly_income,
        credit_score=payload.credit_score,
        loan_amount=payload.loan_amount,
        employment_status=payload.employment_status,
        existing_loans=payload.existing_loans,
        eligibility_result=eligible,
        message=message,
    )

    db.add(application)
    db.commit()

    return {"eligible": eligible, "message": message}


@router.get("/history", response_model=list[LoanHistoryItem])
def loan_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(LoanApplication)
        .filter(LoanApplication.user_id == current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )
    return rows
