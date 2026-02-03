"""
Bookkeeping Service Module
Handles transaction logging, journal entries, and ledger management
"""

from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Types of financial transactions"""
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"


class ExpenseCategory(str, Enum):
    """Expense categories for SMEs"""
    SALARY = "salary"
    RENT = "rent"
    UTILITIES = "utilities"
    MARKETING = "marketing"
    SUPPLIES = "supplies"
    TRAVEL = "travel"
    DEPRECIATION = "depreciation"
    INTEREST = "interest"
    TAX = "tax"
    MAINTENANCE = "maintenance"
    PROFESSIONAL_FEES = "professional_fees"
    OTHER = "other"


class IncomeCategory(str, Enum):
    """Income categories"""
    SALES = "sales"
    SERVICES = "services"
    RENTAL = "rental"
    INTEREST = "interest"
    INVESTMENT = "investment"
    OTHER = "other"


class Transaction:
    """Represents a single transaction"""
    
    def __init__(
        self,
        transaction_id: str,
        date: datetime,
        description: str,
        amount: float,
        transaction_type: TransactionType,
        category: str,
        account: str,
        reference: Optional[str] = None,
        notes: Optional[str] = None
    ):
        self.transaction_id = transaction_id
        self.date = date
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.account = account
        self.reference = reference
        self.notes = notes
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "description": self.description,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "account": self.account,
            "reference": self.reference,
            "notes": self.notes
        }


class JournalEntry:
    """Represents a double-entry journal entry"""
    
    def __init__(
        self,
        entry_id: str,
        date: datetime,
        description: str,
        debit_account: str,
        credit_account: str,
        amount: float,
        reference: Optional[str] = None
    ):
        self.entry_id = entry_id
        self.date = date
        self.description = description
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.amount = amount
        self.reference = reference
    
    def to_dict(self) -> Dict:
        """Convert journal entry to dictionary"""
        return {
            "entry_id": self.entry_id,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "description": self.description,
            "debit_account": self.debit_account,
            "credit_account": self.credit_account,
            "amount": self.amount,
            "reference": self.reference
        }


class Ledger:
    """Account ledger for tracking account balances"""
    
    def __init__(self, account_name: str, account_type: str):
        self.account_name = account_name
        self.account_type = account_type
        self.debit_balance = 0.0
        self.credit_balance = 0.0
        self.entries: List[Dict] = []
    
    def add_debit(self, amount: float, description: str, date: datetime):
        """Add debit entry"""
        self.debit_balance += amount
        self.entries.append({
            "type": "debit",
            "amount": amount,
            "description": description,
            "date": date.isoformat() if isinstance(date, datetime) else date,
            "balance": self.get_balance()
        })
    
    def add_credit(self, amount: float, description: str, date: datetime):
        """Add credit entry"""
        self.credit_balance += amount
        self.entries.append({
            "type": "credit",
            "amount": amount,
            "description": description,
            "date": date.isoformat() if isinstance(date, datetime) else date,
            "balance": self.get_balance()
        })
    
    def get_balance(self) -> float:
        """Calculate account balance based on account type"""
        # Assets, expenses: debit balance is positive
        # Liabilities, equity, income: credit balance is positive
        if self.account_type in ["asset", "expense"]:
            return self.debit_balance - self.credit_balance
        else:
            return self.credit_balance - self.debit_balance
    
    def to_dict(self) -> Dict:
        """Convert ledger to dictionary"""
        return {
            "account_name": self.account_name,
            "account_type": self.account_type,
            "balance": self.get_balance(),
            "debit_total": self.debit_balance,
            "credit_total": self.credit_balance,
            "entries_count": len(self.entries),
            "last_entry_date": self.entries[-1]["date"] if self.entries else None
        }


class BookkeepingService:
    """Service for managing bookkeeping operations"""
    
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.journal_entries: List[JournalEntry] = []
        self.ledgers: Dict[str, Ledger] = {}
        self.transaction_counter = 0
        self.entry_counter = 0
    
    def log_transaction(
        self,
        date: datetime,
        description: str,
        amount: float,
        transaction_type: TransactionType,
        category: str,
        account: str,
        reference: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Transaction:
        """Log a new transaction"""
        self.transaction_counter += 1
        transaction_id = f"TXN-{self.transaction_counter:06d}"
        
        transaction = Transaction(
            transaction_id=transaction_id,
            date=date,
            description=description,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            account=account,
            reference=reference,
            notes=notes
        )
        
        self.transactions.append(transaction)
        return transaction
    
    def create_journal_entry(
        self,
        date: datetime,
        description: str,
        debit_account: str,
        credit_account: str,
        amount: float,
        reference: Optional[str] = None
    ) -> JournalEntry:
        """Create a double-entry journal entry"""
        self.entry_counter += 1
        entry_id = f"JE-{self.entry_counter:06d}"
        
        entry = JournalEntry(
            entry_id=entry_id,
            date=date,
            description=description,
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            reference=reference
        )
        
        self.journal_entries.append(entry)
        
        # Update ledgers
        if debit_account not in self.ledgers:
            self.ledgers[debit_account] = Ledger(debit_account, "asset")
        if credit_account not in self.ledgers:
            self.ledgers[credit_account] = Ledger(credit_account, "liability")
        
        self.ledgers[debit_account].add_debit(amount, description, date)
        self.ledgers[credit_account].add_credit(amount, description, date)
        
        return entry
    
    def get_ledger(self, account_name: str) -> Optional[Dict]:
        """Get ledger for specific account"""
        if account_name in self.ledgers:
            return self.ledgers[account_name].to_dict()
        return None
    
    def get_trial_balance(self) -> Dict:
        """Generate trial balance from all ledgers"""
        trial_balance = {
            "date": datetime.now().isoformat(),
            "accounts": [],
            "total_debits": 0.0,
            "total_credits": 0.0
        }
        
        for account_name, ledger in self.ledgers.items():
            balance = ledger.get_balance()
            ledger_dict = ledger.to_dict()
            
            trial_balance["accounts"].append({
                "account": account_name,
                "debit": ledger.debit_balance if balance > 0 else 0,
                "credit": ledger.credit_balance if balance < 0 else 0,
                "balance": balance
            })
            
            if balance > 0:
                trial_balance["total_debits"] += balance
            else:
                trial_balance["total_credits"] += abs(balance)
        
        # Check if balanced
        trial_balance["is_balanced"] = abs(
            trial_balance["total_debits"] - trial_balance["total_credits"]
        ) < 0.01
        
        return trial_balance
    
    def get_account_summary(self, account_type: Optional[str] = None) -> List[Dict]:
        """Get summary of accounts, optionally filtered by type"""
        summaries = []
        
        for account_name, ledger in self.ledgers.items():
            if account_type and ledger.account_type != account_type:
                continue
            
            summaries.append({
                "account": account_name,
                "type": ledger.account_type,
                "balance": ledger.get_balance(),
                "debit_total": ledger.debit_balance,
                "credit_total": ledger.credit_balance,
                "transactions": len(ledger.entries)
            })
        
        return summaries
    
    def categorize_expenses(self) -> Dict[str, float]:
        """Categorize expenses by type"""
        categories = {}
        
        for transaction in self.transactions:
            if transaction.transaction_type == TransactionType.EXPENSE:
                category = transaction.category
                if category not in categories:
                    categories[category] = 0.0
                categories[category] += transaction.amount
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def categorize_income(self) -> Dict[str, float]:
        """Categorize income by type"""
        categories = {}
        
        for transaction in self.transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                category = transaction.category
                if category not in categories:
                    categories[category] = 0.0
                categories[category] += transaction.amount
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def get_transaction_summary(self) -> Dict:
        """Get overall transaction summary"""
        total_income = 0.0
        total_expenses = 0.0
        total_assets = 0.0
        total_liabilities = 0.0
        
        for transaction in self.transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                total_income += transaction.amount
            elif transaction.transaction_type == TransactionType.EXPENSE:
                total_expenses += transaction.amount
            elif transaction.transaction_type == TransactionType.ASSET:
                total_assets += transaction.amount
            elif transaction.transaction_type == TransactionType.LIABILITY:
                total_liabilities += transaction.amount
        
        return {
            "total_transactions": len(self.transactions),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": total_income - total_expenses,
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "net_worth": total_assets - total_liabilities,
            "expense_categories": self.categorize_expenses(),
            "income_categories": self.categorize_income()
        }
    
    def get_transactions_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get transactions within date range"""
        transactions = [
            t.to_dict() for t in self.transactions
            if start_date <= t.date <= end_date
        ]
        return sorted(transactions, key=lambda x: x["date"])
    
    def validate_books(self) -> Dict:
        """Validate bookkeeping entries"""
        trial_balance = self.get_trial_balance()
        
        return {
            "is_balanced": trial_balance["is_balanced"],
            "total_debits": trial_balance["total_debits"],
            "total_credits": trial_balance["total_credits"],
            "difference": abs(
                trial_balance["total_debits"] - trial_balance["total_credits"]
            ),
            "transaction_count": len(self.transactions),
            "journal_entry_count": len(self.journal_entries),
            "account_count": len(self.ledgers),
            "validation_status": "VALID" if trial_balance["is_balanced"] else "UNBALANCED"
        }


def simple_cashflow_forecast(current_cashflow):
    """Generate a realistic up-and-down forecast pattern"""
    base = current_cashflow
    return [
        base * 1.05,      # Month 1: slight growth
        base * 1.12,      # Month 2: strong growth
        base * 0.95,      # Month 3: dip (seasonal)
        base * 1.08,      # Month 4: recovery
        base * 1.15,      # Month 5: strong
        base * 0.98,      # Month 6: slight dip
        base * 1.18,      # Month 7: peak
        base * 1.10,      # Month 8: stabilize
        base * 1.22,      # Month 9: growth again
        base * 1.05,      # Month 10: slight decline
        base * 1.20,      # Month 11: recovery
        base * 1.25       # Month 12: strong finish
    ]
