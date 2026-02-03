def detect_financial_risks(revenue, expenses, receivables_days):
    risks = []

    if expenses > revenue:
        risks.append("Operating at a loss (burn rate risk)")

    if expenses > revenue * 1.2:
        risks.append("Sudden expense spike detected")

    if receivables_days > 60:
        risks.append("Receivable delay risk")

    return risks
