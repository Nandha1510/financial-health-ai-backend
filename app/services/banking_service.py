# app/services/banking_service.py

import os
import requests

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY_ID", "demo_key")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET", "demo_secret")

def fetch_bank_account_summary(customer_id: str):
    """
    Razorpay Banking Integration (Mock for Hackathon)
    Replace with real RazorpayX APIs in production.
    """

    # --- MOCK RESPONSE (used for demo) ---
    return {
        "provider": "Razorpay",
        "customer_id": customer_id,
        "average_balance": 280000,
        "monthly_inflow": 620000,
        "monthly_outflow": 450000,
        "transactions_count": 85
    }

def get_bank_products(credit_score):
    """Get bank products based on credit score"""
    products = {
        "AAA": [
            {"name": "Premium Business Loan", "rate": "7-9%", "amount": "25L-1Cr"},
            {"name": "Working Capital Facility", "rate": "6-8%", "amount": "10L-50L"}
        ],
        "AA": [
            {"name": "Business Loan", "rate": "9-11%", "amount": "15L-75L"},
            {"name": "Overdraft", "rate": "10-12%", "amount": "5L-25L"}
        ],
        "A": [
            {"name": "Term Loan", "rate": "12-14%", "amount": "5L-25L"}
        ]
    }
    
    if credit_score >= 750:
        rating = "AAA"
    elif credit_score >= 650:
        rating = "AA"
    elif credit_score >= 550:
        rating = "A"
    else:
        rating = "D"
    
    return products.get(rating, [])

def calculate_loan_emi(principal, rate, tenure):
    """Calculate monthly EMI"""
    monthly_rate = rate / 12 / 100
    months = tenure * 12
    
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    return round(emi, 2)
