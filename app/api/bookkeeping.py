"""
Bookkeeping API Endpoints
Handles transaction logging, journal entries, and accounting operations
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.services.bookkeeping import (
    BookkeepingService,
    TransactionType,
    ExpenseCategory,
    IncomeCategory
)

router = APIRouter()

# In-memory service instance (replace with database in production)
bookkeeping_service = BookkeepingService()


class TransactionRequest(BaseModel):
    """Request model for creating a transaction"""
    date: str  # ISO format datetime
    description: str
    amount: float
    transaction_type: str  # income, expense, asset, liability, equity
    category: str
    account: str
    reference: Optional[str] = None
    notes: Optional[str] = None


class JournalEntryRequest(BaseModel):
    """Request model for creating a journal entry"""
    date: str  # ISO format datetime
    description: str
    debit_account: str
    credit_account: str
    amount: float
    reference: Optional[str] = None


@router.post("/bookkeeping/transaction", tags=["Bookkeeping"])
async def log_transaction(request: TransactionRequest):
    """Log a new financial transaction"""
    try:
        date = datetime.fromisoformat(request.date)
        transaction = bookkeeping_service.log_transaction(
            date=date,
            description=request.description,
            amount=request.amount,
            transaction_type=TransactionType(request.transaction_type),
            category=request.category,
            account=request.account,
            reference=request.reference,
            notes=request.notes
        )
        return {
            "success": True,
            "transaction": transaction.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid transaction data: {str(e)}")


@router.post("/bookkeeping/journal-entry", tags=["Bookkeeping"])
async def create_journal_entry(request: JournalEntryRequest):
    """Create a double-entry journal entry"""
    try:
        date = datetime.fromisoformat(request.date)
        entry = bookkeeping_service.create_journal_entry(
            date=date,
            description=request.description,
            debit_account=request.debit_account,
            credit_account=request.credit_account,
            amount=request.amount,
            reference=request.reference
        )
        return {
            "success": True,
            "entry": entry.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid journal entry data: {str(e)}")


@router.get("/bookkeeping/ledger/{account_name}", tags=["Bookkeeping"])
async def get_ledger(account_name: str):
    """Get ledger for a specific account"""
    ledger = bookkeeping_service.get_ledger(account_name)
    
    if not ledger:
        raise HTTPException(status_code=404, detail=f"Account '{account_name}' not found")
    
    return {
        "success": True,
        "ledger": ledger
    }


@router.get("/bookkeeping/trial-balance", tags=["Bookkeeping"])
async def get_trial_balance():
    """Generate trial balance from all accounts"""
    balance = bookkeeping_service.get_trial_balance()
    return {
        "success": True,
        "trial_balance": balance
    }


@router.get("/bookkeeping/accounts", tags=["Bookkeeping"])
async def get_accounts(account_type: Optional[str] = None):
    """Get summary of all accounts, optionally filtered by type"""
    accounts = bookkeeping_service.get_account_summary(account_type)
    
    return {
        "success": True,
        "accounts": accounts,
        "total_accounts": len(accounts)
    }


@router.get("/bookkeeping/transaction-summary", tags=["Bookkeeping"])
async def get_transaction_summary():
    """Get overall transaction summary with categorized income and expenses"""
    summary = bookkeeping_service.get_transaction_summary()
    
    return {
        "success": True,
        "summary": summary
    }


@router.get("/bookkeeping/expenses", tags=["Bookkeeping"])
async def get_expense_breakdown():
    """Get expenses categorized by type"""
    expenses = bookkeeping_service.categorize_expenses()
    
    total = sum(expenses.values())
    
    return {
        "success": True,
        "expenses": expenses,
        "total_expenses": total,
        "categories": len(expenses)
    }


@router.get("/bookkeeping/income", tags=["Bookkeeping"])
async def get_income_breakdown():
    """Get income categorized by type"""
    income = bookkeeping_service.categorize_income()
    
    total = sum(income.values())
    
    return {
        "success": True,
        "income": income,
        "total_income": total,
        "sources": len(income)
    }


@router.post("/bookkeeping/validate", tags=["Bookkeeping"])
async def validate_books():
    """Validate all bookkeeping entries (checks if trial balance is balanced)"""
    validation = bookkeeping_service.validate_books()
    
    return {
        "success": True,
        "validation": validation
    }


@router.get("/bookkeeping/categories/expense", tags=["Bookkeeping"])
async def get_expense_categories():
    """Get list of available expense categories"""
    categories = [category.value for category in ExpenseCategory]
    
    return {
        "success": True,
        "categories": categories
    }


@router.get("/bookkeeping/categories/income", tags=["Bookkeeping"])
async def get_income_categories():
    """Get list of available income categories"""
    categories = [category.value for category in IncomeCategory]
    
    return {
        "success": True,
        "categories": categories
    }


@router.post("/bookkeeping/period-summary", tags=["Bookkeeping"])
async def get_period_summary(start_date: str, end_date: str):
    """Get transaction summary for a specific period"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        transactions = bookkeeping_service.get_transactions_by_date_range(start, end)
        
        total_amount = sum(t["amount"] for t in transactions)
        
        return {
            "success": True,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "transactions": transactions,
            "total_transactions": len(transactions),
            "total_amount": total_amount
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
