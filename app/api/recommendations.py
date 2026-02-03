from fastapi import APIRouter
from app.ai.cost_optimizer import cost_optimization

router = APIRouter()

@router.post("/")
def get_recommendations(
    expense_ratio: float,
    industry_avg: float
):
    message = cost_optimization(expense_ratio, industry_avg)
    return {
        "recommendation": message
    }


