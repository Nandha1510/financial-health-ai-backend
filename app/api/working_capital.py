from fastapi import APIRouter
from app.services.working_capital import analyze_working_capital, optimize_receivables, optimize_inventory, optimize_payables

router = APIRouter()

@router.post("/analysis")
def analyze_wc(
    revenue: float,
    receivables_days: int = 45,
    payables_days: int = 30,
    inventory_days: int = 40
):
    """Analyze working capital efficiency"""
    return analyze_working_capital(revenue, receivables_days, payables_days, inventory_days)

@router.post("/receivables-optimization")
def optimize_ar(total_receivables: float, current_dso: int = 60, target_dso: int = 45):
    """Optimize receivables collection"""
    return optimize_receivables(total_receivables, current_dso, target_dso)

@router.post("/inventory-optimization")
def optimize_inv(annual_cogs: float, current_dio: int = 50, target_dio: int = 30):
    """Optimize inventory levels"""
    return optimize_inventory(annual_cogs, current_dio, target_dio)

@router.post("/payables-optimization")
def optimize_ap(annual_cogs: float, current_dpo: int = 30, target_dpo: int = 45):
    """Optimize payables period"""
    return optimize_payables(annual_cogs, current_dpo, target_dpo)
