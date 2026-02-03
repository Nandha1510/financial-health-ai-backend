def creditworthiness_metrics(
    operating_income,
    debt_payments,
    assets,
    liabilities,
    equity,
    profitability_ratio=0.15
):
    """Calculate creditworthiness metrics and generate credit score"""
    dscr = operating_income / debt_payments if debt_payments else 1.0
    current_ratio = assets / liabilities if liabilities else 2.0
    debt_equity = liabilities / equity if equity else 0.5
    
    # Calculate credit score (300-900 scale)
    credit_score = calculate_credit_score(dscr, current_ratio, debt_equity, profitability_ratio)

    return {
        "DSCR": round(dscr, 2),
        "current_ratio": round(current_ratio, 2),
        "debt_equity": round(debt_equity, 2),
        "credit_score": credit_score["score"],
        "credit_rating": credit_score["rating"],
        "recommendation": credit_score["recommendation"]
    }

def calculate_credit_score(dscr, current_ratio, debt_equity, profitability):
    """Calculate credit score using weighted metrics (300-900 scale)"""
    # Normalize each metric to 0-100 scale
    dscr_score = min(100, max(0, (dscr / 1.5) * 100))
    
    if current_ratio >= 2.0:
        liquidity_score = 100
    elif current_ratio >= 1.5:
        liquidity_score = 80
    elif current_ratio >= 1.0:
        liquidity_score = 50
    else:
        liquidity_score = 20
    
    if debt_equity < 0.5:
        solvency_score = 100
    elif debt_equity < 1.5:
        solvency_score = 80
    elif debt_equity < 2.5:
        solvency_score = 50
    else:
        solvency_score = 20
    
    if profitability > 0.2:
        profit_score = 100
    elif profitability > 0.1:
        profit_score = 75
    elif profitability > 0.05:
        profit_score = 50
    elif profitability > 0:
        profit_score = 25
    else:
        profit_score = 0
    
    # Weighted average
    score_100 = (dscr_score * 0.30 + liquidity_score * 0.25 + 
                 solvency_score * 0.20 + profit_score * 0.25)
    
    # Convert to 300-900 scale
    credit_score = 300 + (score_100 / 100) * 600
    
    # Determine rating
    if credit_score >= 750:
        rating = "AAA"
        recommendation = "Excellent creditworthiness. Eligible for premium products."
    elif credit_score >= 650:
        rating = "AA"
        recommendation = "Good creditworthiness. Eligible for standard products."
    elif credit_score >= 550:
        rating = "A"
        recommendation = "Average creditworthiness. Limited product availability."
    elif credit_score >= 450:
        rating = "BBB"
        recommendation = "Below average. Work on improving metrics."
    else:
        rating = "D"
        recommendation = "Poor creditworthiness. Improve finances before seeking loans."
    
    return {
        "score": round(credit_score, 0),
        "rating": rating,
        "recommendation": recommendation
    }

def get_recommended_products(credit_score):
    """Get loan products based on credit score"""
    products = {
        "AAA": [
            {"name": "Premium Business Loan", "amount": "25L-1Cr", "rate": "7-9%", "tenure": "3-7 years"},
            {"name": "Working Capital Facility", "amount": "10L-50L", "rate": "6-8%", "tenure": "1-3 years"},
            {"name": "Trade Credit Line", "amount": "5L-25L", "rate": "5-7%", "tenure": "Revolving"}
        ],
        "AA": [
            {"name": "Business Loan", "amount": "15L-75L", "rate": "9-11%", "tenure": "3-7 years"},
            {"name": "Working Capital Loan", "amount": "5L-25L", "rate": "10-12%", "tenure": "1-3 years"}
        ],
        "A": [
            {"name": "Term Loan", "amount": "5L-25L", "rate": "12-14%", "tenure": "3-5 years"},
            {"name": "Unsecured Business Loan", "amount": "2L-10L", "rate": "14-16%", "tenure": "2-4 years"}
        ],
        "BBB": [
            {"name": "Micro Business Loan", "amount": "50K-5L", "rate": "16-18%", "tenure": "2-3 years"}
        ],
        "D": []
    }
    
    if credit_score >= 750:
        rating = "AAA"
    elif credit_score >= 650:
        rating = "AA"
    elif credit_score >= 550:
        rating = "A"
    elif credit_score >= 450:
        rating = "BBB"
    else:
        rating = "D"
    
    return products.get(rating, [])
