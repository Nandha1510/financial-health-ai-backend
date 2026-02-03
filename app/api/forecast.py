from fastapi import APIRouter
from app.services.bookkeeping import simple_cashflow_forecast

router = APIRouter()

@router.post("/")
def forecast_cashflow(current_cashflow: float):
    forecast = simple_cashflow_forecast(current_cashflow)
    return {
        "forecast": forecast
    }
