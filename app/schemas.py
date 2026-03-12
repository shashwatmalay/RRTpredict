from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoanCheckRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    monthly_income: float = Field(gt=0)
    credit_score: int = Field(ge=300, le=900)
    loan_amount: float = Field(gt=0)
    employment_status: str = Field(min_length=2, max_length=100)
    existing_loans: int = Field(ge=0)


class LoanCheckResponse(BaseModel):
    eligible: bool
    message: str


class LoanHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    age: int
    income: float
    credit_score: int
    loan_amount: float
    employment_status: str
    existing_loans: int
    eligibility_result: bool
    message: str
    created_at: datetime


class MessageResponse(BaseModel):
    message: str
