from fastapi import APIRouter
from app.ai.risk_detection import detect_financial_risks

router = APIRouter()

@router.post("/detect")
def risk_analysis(
    revenue: float,
    expenses: float,
    receivables_days: int
):
    risks = detect_financial_risks(
        revenue,
        expenses,
        receivables_days
    )
    return {"risks": risks}
