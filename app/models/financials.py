from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base

class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    revenue = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    assets = Column(Float, nullable=False)
    liabilities = Column(Float, nullable=False)

    industry = Column(String(100))
    currency = Column(String(10), default="INR")

    created_at = Column(DateTime, default=datetime.utcnow)
