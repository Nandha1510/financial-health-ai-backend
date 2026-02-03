from fastapi import APIRouter
from app.services.tax_compliance_service import check_income_tax_compliance, check_gst_filing_compliance, calculate_deductions, check_compliance_calendar, generate_tax_compliance_report
from app.services.working_capital import analyze_working_capital, optimize_receivables, optimize_payables

router = APIRouter()

@router.post("/income-tax")
def check_income_tax(annual_income: float, filing_status: str = "not_filed"):
    """Check income tax compliance"""
    return check_income_tax_compliance(annual_income, filing_status)

@router.post("/gst-compliance")
def check_gst(turnover: float, gstr1_filed: bool = False, gstr3b_filed: bool = False):
    """Check GST filing compliance"""
    return {
        "turnover": turnover,
        "requires_gst": turnover > 1500000,
        "alerts": check_gst_filing_compliance(turnover, gstr1_filed, gstr3b_filed)
    }

@router.post("/deductions")
def get_deductions(business_income: float):
    """Calculate allowed deductions"""
    return calculate_deductions(business_income)

@router.get("/compliance-calendar")
def get_calendar():
    """Get tax compliance calendar"""
    return {"deadlines": check_compliance_calendar()}

@router.post("/tax-report")
def generate_report(revenue: float, expenses: float):
    """Generate comprehensive tax compliance report"""
    financial_data = {"revenue": revenue, "expenses": expenses}
    return generate_tax_compliance_report(financial_data)
