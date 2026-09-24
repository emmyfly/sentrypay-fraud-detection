"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Dict

class TransactionRequest(BaseModel):
    """Request schema for transaction fraud scoring."""
    account_id: str = Field(..., description="Sender account ID")
    device_id: str = Field(..., description="Device ID used for transaction")
    sim_id: str = Field(..., description="SIM card ID")
    recipient_id: str = Field(..., description="Recipient account ID")
    amount: float = Field(..., gt=0, description="Transaction amount in Naira")
    hour_of_day: int = Field(..., ge=0, le=23, description="Hour of transaction (0-23)")
    is_known_recipient: bool = Field(..., description="Whether recipient has been sent money before")
    days_since_device_change: int = Field(..., ge=0, description="Days since device was changed")
    days_since_sim_change: int = Field(..., ge=0, description="Days since SIM card was changed")
    recipient_transfer_count: int = Field(..., ge=0, description="Number of prior transfers to this recipient")
    
    class Config:
        json_schema_extra = {
            "example": {
                "account_id": "ACC000123",
                "device_id": "DEV000456",
                "sim_id": "SIM000789",
                "recipient_id": "RCP000321",
                "amount": 15000.00,
                "hour_of_day": 14,
                "is_known_recipient": True,
                "days_since_device_change": 120,
                "days_since_sim_change": 180,
                "recipient_transfer_count": 5
            }
        }


class RecipientRiskRequest(BaseModel):
    """Request schema for recipient-side mule account detection."""
    recipient_id: str = Field(..., description="Recipient account ID to check")
    num_transactions: int = Field(..., ge=0, description="Total number of received transactions")
    avg_amount: float = Field(..., gt=0, description="Average amount received")
    days_span: int = Field(..., ge=0, description="Days span of transaction history")
    unique_senders_30d: int = Field(..., ge=0, description="Number of unique senders in last 30 days")
    first_time_senders_30d: int = Field(..., ge=0, description="Number of first-time senders in last 30 days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient_id": "RCP000100",
                "num_transactions": 25,
                "avg_amount": 8500.00,
                "days_span": 90,
                "unique_senders_30d": 5,
                "first_time_senders_30d": 1
            }
        }


class RiskResponse(BaseModel):
    """Response schema for risk scoring."""
    score: int = Field(..., ge=0, le=100, description="Risk score from 0 (safe) to 100 (high risk)")
    verdict: str = Field(..., description="Risk verdict: 'safe', 'watch', or 'block'")
    signal_breakdown: Dict[str, float] = Field(..., description="Feature importances from the model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 23,
                "verdict": "safe",
                "signal_breakdown": {
                    "days_since_sim_change": 0.25,
                    "amount": 0.18,
                    "is_known_recipient": 0.15
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API health status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok"
            }
        }
