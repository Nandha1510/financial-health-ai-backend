from fastapi import HTTPException

def validate_email(email: str):
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    return email

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long (max 72 bytes)"
        )

    return password

def validate_financials(revenue, expenses, assets, liabilities):
    if any(v < 0 for v in [revenue, expenses, assets, liabilities]):
        raise HTTPException(
            status_code=400,
            detail="Financial values cannot be negative"
        )
