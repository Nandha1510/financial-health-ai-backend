from fastapi import APIRouter
from app.utils.validators import validate_financials

router = APIRouter()

@router.post("/health-score")
def financial_health_score(
    revenue: float,
    expenses: float,
    assets: float,
    liabilities: float,
    cashflow: float
):
    validate_financials(revenue, expenses, assets, liabilities)

    profitability = max((revenue - expenses) / revenue, 0)
    liquidity = assets / liabilities if liabilities else 1
    leverage = 1 - (liabilities / assets) if assets else 0
    cashflow_score = max(cashflow / revenue, 0)

    score = (
        liquidity * 0.25 +
        profitability * 0.30 +
        leverage * 0.20 +
        cashflow_score * 0.25
    ) * 100

    return {
        "financial_health_score": round(score, 2)
    }

