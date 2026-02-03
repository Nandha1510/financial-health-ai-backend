# app/models/reports.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class FinancialReport(Base):
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    report_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
