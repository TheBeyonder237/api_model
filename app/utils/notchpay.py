import requests
from app.core.config import settings


def initiate_payment(amount: int, currency: str, email: str):
    url = "https://api.notchpay.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {settings.NOTCHPAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "email": email
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def verify_payment(payment_id: str):
    url = f"https://api.notchpay.com/v1/payments/{payment_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.NOTCHPAY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()
