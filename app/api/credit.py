from fastapi import APIRouter
from app.ai.credit_scoring import creditworthiness_metrics, calculate_credit_score, get_recommended_products
from app.services.banking_service import get_bank_products, calculate_loan_emi

router = APIRouter()

@router.post("/evaluate")
def evaluate_credit(
    operating_income: float,
    debt_payments: float,
    assets: float,
    liabilities: float,
    equity: float,
    profitability: float = 0.15
):
    """Evaluate creditworthiness with detailed metrics"""
    metrics = creditworthiness_metrics(
        operating_income, debt_payments, assets, liabilities, equity, profitability
    )
    return metrics

@router.post("/credit-score")
def calculate_credit(
    dscr: float = 1.5,
    current_ratio: float = 1.8,
    debt_equity: float = 0.8,
    profitability: float = 0.15
):
    """Calculate credit score (300-900 scale) with rating"""
    score_data = calculate_credit_score(dscr, current_ratio, debt_equity, profitability)
    products = get_recommended_products(score_data["score"])
    
    return {
        "credit_score": score_data["score"],
        "rating": score_data["rating"],
        "recommendation": score_data["recommendation"],
        "recommended_products": products
    }

@router.post("/loan-products")
def get_products(credit_score: float = 750):
    """Get loan products based on credit score"""
    return {
        "credit_score": credit_score,
        "products": get_bank_products(credit_score)
    }

@router.post("/loan-emi")
def calculate_emi(
    principal: float,
    annual_rate: float = 10.0,
    tenure_years: int = 5
):
    """Calculate monthly EMI for loans"""
    emi_data = calculate_loan_emi(principal, annual_rate, tenure_years)
    return emi_data

@router.get("/bank-options")
def get_bank_options():
    """Get available banking products"""
    return {
        "options": [
            {
                "name": "HDFC Bank",
                "loan_type": "Premium Business Loan",
                "rate": "7-9%",
                "amount": "25L-1Cr"
            },
            {
                "name": "ICICI Bank",
                "loan_type": "Business Loan",
                "rate": "8-10%",
                "amount": "10L-75L"
            },
            {
                "name": "SBI",
                "loan_type": "Term Loan",
                "rate": "9-11%",
                "amount": "5L-50L"
            },
            {
                "name": "Razorpay",
                "loan_type": "Digital Loan",
                "rate": "10-13%",
                "amount": "2L-30L"
            }
        ]
    }


@router.get("/ratings")
def get_ratings():
    """Get credit ratings guide"""
    return {
        "ratings": [
            {"rating": "AAA", "score": "750+", "description": "Excellent credit"},
            {"rating": "AA", "score": "650-749", "description": "Very Good credit"},
            {"rating": "A", "score": "550-649", "description": "Good credit"},
            {"rating": "BBB", "score": "450-549", "description": "Acceptable credit"},
            {"rating": "D", "score": "<450", "description": "Poor credit"}
        ]
    }
