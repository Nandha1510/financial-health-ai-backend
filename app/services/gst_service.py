# app/services/gst_service.py

def fetch_gst_returns(gstin: str):
    """
    GSTN Integration (Simulated)
    In production, this connects to GST Suvidha Provider (GSP).
    """

    return {
        "gstin": gstin,
        "months_filed": 10,
        "expected_months": 12,
        "reported_turnover": 8200000,
        "tax_paid": 1476000,
        "itc_claimed": 980000
    }


def gst_compliance_analysis(revenue, gst_data):
    alerts = []

    if gst_data["months_filed"] < gst_data["expected_months"]:
        alerts.append("Missing GST filings detected")

    if gst_data["reported_turnover"] != revenue:
        alerts.append("Revenue mismatch with GST returns")

    if gst_data["itc_claimed"] < revenue * 0.12:
        alerts.append("Possible ITC underutilization")

    return alerts
