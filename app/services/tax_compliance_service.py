# Tax Compliance Service for Indian SMEs

def check_income_tax_compliance(annual_income, filing_status="not_filed"):
    """Check income tax filing compliance and recommendations"""
    alerts = []
    recommendations = []
    
    # Tax slab calculation (FY 2024-25 Indian tax slabs - New Regime)
    if annual_income > 3000000:
        tax_payable = (annual_income * 0.30)  # Simplified
        alerts.append("Income exceeds 30L - ensure proper tax filing")
        recommendations.append("File ITR-1 or ITR-2 immediately")
    elif annual_income > 500000:
        tax_payable = (annual_income * 0.20)
        if filing_status == "not_filed":
            alerts.append(f"Income {annual_income} requires ITR filing")
    else:
        tax_payable = 0
        if annual_income > 250000:
            recommendations.append("Consider filing ITR for tax planning")
    
    # GST compliance check
    gst_alerts = check_gst_filing_compliance(annual_income)
    alerts.extend(gst_alerts)
    
    return {
        "income": annual_income,
        "estimated_tax": round(tax_payable, 2),
        "filing_required": annual_income > 250000,
        "alerts": alerts,
        "recommendations": recommendations
    }

def check_gst_filing_compliance(turnover, gstr1_filed=False, gstr3b_filed=False):
    """Check GST filing compliance"""
    alerts = []
    
    # GST registration threshold
    if turnover > 4000000:  # 40 Lakhs
        if not gstr1_filed:
            alerts.append("GSTR-1 (sales return) not filed - Required monthly")
        if not gstr3b_filed:
            alerts.append("GSTR-3B (summary return) not filed - Required monthly")
    elif turnover > 1500000:  # 15 Lakhs
        alerts.append("Eligible for GST registration - Consider registering")
    
    return alerts

def check_tds_compliance(total_vendor_payments, payments_by_vendor=None):
    """Check TDS (Tax Deducted at Source) compliance"""
    alerts = []
    
    # TDS rates for Indian tax law
    if total_vendor_payments > 1000000:  # More than 10L
        alerts.append("High vendor payments - Verify TDS compliance (10% on contractor payments)")
    
    return alerts

def calculate_deductions(business_income, expense_category=None):
    """Calculate allowable deductions under Indian tax law"""
    deductions = {
        "salary_wages": min(business_income * 0.40, 2500000),  # Salary can be up to 40%
        "rent": min(business_income * 0.15, 1000000),
        "electricity": min(business_income * 0.05, 500000),
        "depreciation": business_income * 0.10,
        "professional_fees": min(business_income * 0.05, 250000),
        "insurance": min(business_income * 0.03, 150000),
    }
    
    total_deductions = sum(deductions.values())
    taxable_income = max(business_income - total_deductions, 0)
    
    return {
        "deductions": deductions,
        "total_deductions": round(total_deductions, 2),
        "taxable_income": round(taxable_income, 2)
    }

def check_compliance_calendar():
    """Return important tax filing deadlines"""
    return {
        "quarterly_gst_filing": "Last day of next month (Monthly/Quarterly)",
        "quarterly_tds_return": "15th of next month",
        "annual_itr_filing": "31st July",
        "annual_gst_annual_return": "31st December",
        "fy_end": "31st March",
        "half_yearly_provisions": "30th September"
    }

def generate_tax_compliance_report(financial_data):
    """Generate comprehensive tax compliance report"""
    annual_income = financial_data.get("revenue", 0)
    expenses = financial_data.get("expenses", 0)
    
    it_compliance = check_income_tax_compliance(annual_income)
    tds_compliance = check_tds_compliance(expenses)
    deductions = calculate_deductions(annual_income)
    calendar = check_compliance_calendar()
    
    return {
        "income_tax": it_compliance,
        "tds": {"alerts": tds_compliance},
        "deductions": deductions,
        "filing_calendar": calendar,
        "status": "compliant" if not it_compliance["alerts"] else "needs_attention"
    }
