from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import hmac
import hashlib
import os
import uuid
import requests


router = APIRouter()

RAZORPAY_KEY = os.environ.get("RAZORPAY_KEY", "")
RAZORPAY_SECRET = os.environ.get("RAZORPAY_SECRET", "")

@router.post("/create-order")
async def create_razorpay_order(request: Request):
    """Create a Razorpay order for the frontend to use in checkout.
    Expects JSON with: amount (in INR), description
    For demo/test purposes, returns a mock order ID.
    """
    try:
        payload = await request.json()
        amount = payload.get("amount")
        description = payload.get("description", "Payment via FinHealth AI")
        
        if not amount or amount <= 0:
            return JSONResponse(status_code=400, content={"detail": "Invalid amount"})
        
        # Generate a mock order ID for testing
        # In production, this would call Razorpay API
        order_id = f"order_{uuid.uuid4().hex[:8]}"
        
        return JSONResponse(status_code=200, content={
            "success": True,
            "order_id": order_id,
            "amount": amount,
            "currency": "INR"
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@router.post("/verify")
async def verify_payment(request: Request):
    """Verify Razorpay payment signature sent from frontend checkout.
    Expects JSON with: razorpay_order_id, razorpay_payment_id, razorpay_signature
    """
    payload = await request.json()
    order_id = payload.get("razorpay_order_id")
    payment_id = payload.get("razorpay_payment_id")
    signature = payload.get("razorpay_signature")

    if not (order_id and payment_id and signature):
        return JSONResponse(status_code=400, content={"detail": "Missing payment fields"})

    if not RAZORPAY_SECRET:
        return JSONResponse(status_code=500, content={"detail": "Razorpay secret not configured on server"})

    # Compute expected signature
    msg = f"{order_id}|{payment_id}".encode()
    expected_signature = hmac.new(RAZORPAY_SECRET.encode(), msg, hashlib.sha256).hexdigest()

    if hmac.compare_digest(expected_signature, signature):
        # TODO: persist payment record to DB if desired
        return JSONResponse(status_code=200, content={"success": True})
    else:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Invalid signature"})
