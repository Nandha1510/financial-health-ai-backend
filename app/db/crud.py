from sqlalchemy.orm import Session
from app.models.user import User
from app.models.financials import FinancialStatement

# ---------------- USER CRUD ----------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    user = User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------------- FINANCIAL CRUD ----------------

def create_financial_statement(
    db: Session,
    user_id: int,
    revenue: float,
    expenses: float,
    assets: float,
    liabilities: float,
    industry: str
):
    record = FinancialStatement(
        user_id=user_id,
        revenue=revenue,
        expenses=expenses,
        assets=assets,
        liabilities=liabilities,
        industry=industry
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_financials_by_user(db: Session, user_id: int):
    return db.query(FinancialStatement).filter(
        FinancialStatement.user_id == user_id
    ).all()
