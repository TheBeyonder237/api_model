from datetime import timedelta, date

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.payment import PaymentInitializeRequest, PaymentInitializeResponse, PaymentStatusRequest, PaymentStatusResponse
from app.core.config import settings
from sqlalchemy.orm import Session
from app import models, schemas
import httpx
from app.schemas.payment import PaymentUpdateRequest, PaymentUpdateResponse, Business, Customer, Transaction
import uuid

router = APIRouter()


@router.post("/initialize_payment", response_model=PaymentInitializeResponse)
async def initialize_payment(payment_request: PaymentInitializeRequest):
    """
    Endpoint pour initialiser un paiement.
    """
    headers = {
        "Authorization": settings.API_KEY,
        "Accept": "application/json",
    }
    data = payment_request.dict()

    transaction_reference = f"trx_{uuid.uuid4().hex}"

    # Ajouter la référence générée à la donnée envoyée à l'API NotchPay
    data["reference"] = transaction_reference

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{settings.NOTCHPAY_API_URL}/initialize", headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            # Log de la réponse complète pour le débogage
            print("Réponse de l'API NotchPay:", response_data)

            # Adapter la réponse pour correspondre au modèle attendu
            transaction_data = response_data.get("transaction", {})
            transaction_data['business'] = {
                'id': '9pDOCy7Rp',
                'country': 'CM',
                'email': 'hello@notchpay.co',
                'phone': '+237 6 55******',
                'poster': None,
                'name': 'Notch Africa'
            }
            transaction_data['customer'] = {
                'id': transaction_data.get('customer', ''),
                'name': None,
                'email': 'customer@email.com',
                'sandbox': False,
                'phone': None,
                'blocked': False
            }
            transaction_data['initiated_at'] = response_data.get('created_at', '')
            transaction_data['updated_at'] = response_data.get('created_at', '')

            # Extraire l'URL de paiement
            payment_url = response_data.get("authorization_url")

            if payment_url:
                return PaymentInitializeResponse(
                    status=response_data.get("status"),
                    message=response_data.get("message"),
                    code=response_data.get("code"),
                    transaction=transaction_data,
                    payment_url=payment_url
                )
            else:
                raise HTTPException(status_code=500, detail="Impossible de récupérer l'URL de paiement")
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json()  # Extraire les détails de l'erreur
            raise HTTPException(status_code=e.response.status_code,
                                detail=f"Erreur lors de l'initialisation du paiement: {error_detail}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@router.post("/payment_status", response_model=PaymentStatusResponse)
async def payment_status(status_request: PaymentStatusRequest):
    """
    Endpoint pour vérifier le statut d'un paiement.
    """
    headers = {
        "Authorization": settings.API_KEY,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.NOTCHPAY_API_URL}/{status_request.reference}", headers=headers)
            response.raise_for_status()
            response_data = response.json()

            print("Réponse de l'API NotchPay:", response_data)

            # Extraire et structurer les données de la transaction
            transaction_data = response_data.get("transaction", {})
            customer_data = {
                'id': transaction_data.get('customer'),
                'name': "User test",  # Nom de l'utilisateur à définir
                'email': "customer@email.com",  # Email de l'utilisateur à définir
                'sandbox': transaction_data.get('sandbox', False),
                'phone': None,
                'blocked': False
            }

            business_data = {
                'id': '9pDOCy7Rp',
                'country': 'CM',
                'email': 'hello@notchpay.co',
                'phone': '+237 6 55 72 82 67',
                'poster': None,
                'name': 'Notch Africa'
            }

            transaction = Transaction(
                amount=transaction_data.get("amount"),
                amount_total=transaction_data.get("amount_total"),
                sandbox=transaction_data.get("sandbox"),
                fee=transaction_data.get("fee"),
                converted_amount=transaction_data.get("converted_amount"),
                business=Business(**business_data),
                customer=Customer(**customer_data),
                description=transaction_data.get("description"),
                reference=transaction_data.get("reference"),
                merchant_reference=transaction_data.get("merchant_reference"),
                status=transaction_data.get("status"),
                currency=transaction_data.get("currency"),
                initiated_at=transaction_data.get("created_at"),
                updated_at=transaction_data.get("created_at")  # Assuming created_at is the same as updated_at
            )

            return PaymentStatusResponse(
                code=response_data.get("code"),
                status=response_data.get("status"),
                message=response_data.get("message"),
                transaction=transaction
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Erreur lors de la vérification du statut du paiement")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@router.put("/payments/{reference}", response_model=PaymentUpdateResponse)
async def update_payment(reference: str, payment_update: PaymentUpdateRequest):
    """
    Endpoint pour mettre à jour un paiement.
    """
    headers = {
        "Authorization": settings.API_KEY,
        "Accept": "application/json",
    }
    data = {
        "channel": "cm.mobile",
        "data": {
            "phone": payment_update.phone
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{settings.NOTCHPAY_API_URL}/{reference}", headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            print("Réponse de l'API NotchPay:", response_data)

            return PaymentUpdateResponse(
                message=response_data.get("message"),
                code=response_data.get("code"),
                status=response_data.get("status"),
                action=response_data.get("action")
            )
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json()
            raise HTTPException(status_code=e.response.status_code,
                                detail=f"Erreur lors de la mise à jour du paiement: {error_detail}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


