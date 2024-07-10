from pydantic import BaseModel, EmailStr, Field
from typing import Dict
from typing import Optional, Dict, Any

class PaymentStatusRequest(BaseModel):
    reference: str

class Customer(BaseModel):
    id: str
    name: Optional[str]
    email: str
    sandbox: bool
    phone: Optional[str] = None
    blocked: bool

class Business(BaseModel):
    id: str
    country: str
    email: str
    phone: str
    poster: Optional[str] = None
    name: str

class Transaction(BaseModel):
    amount: int
    amount_total: int
    sandbox: bool
    fee: int
    converted_amount: int
    business: Business
    customer: Customer
    description: str
    reference: str
    merchant_reference: str
    status: str
    currency: str
    initiated_at: str
    updated_at: str

class PaymentStatusResponse(BaseModel):
    code: int
    status: str
    message: str
    transaction: Transaction


class PaymentInitializeResponse(BaseModel):
    status: str
    message: str
    code: int
    transaction: Transaction
    payment_url: str

class PaymentInitializeRequest(BaseModel):
    email: EmailStr
    currency: str = Field(..., max_length=3, description="Code de la monnaie (ex: USD, EUR)")
    amount: float = Field(..., gt=0, description="Montant à payer")
    phone: str = Field(..., max_length=15, description="Numéro de téléphone du payeur")
    description: str = Field(..., max_length=255, description="Description du paiement")


class PaymentStatusRequest(BaseModel):
    reference: str = Field(..., max_length=100, description="Référence unique du paiement")


class PaymentCreate(PaymentInitializeRequest):
    pass


class PaymentStatus(BaseModel):
    reference: str
    status: str


class PaymentUpdateRequest(BaseModel):
    phone: str


class PaymentUpdateResponse(BaseModel):
    message: str
    code: int
    status: str
    action: str