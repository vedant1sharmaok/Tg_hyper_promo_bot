from fastapi import APIRouter
from .endpoints import campaigns_api

api_router = APIRouter()
api_router.include_router(campaigns_api, prefix="/campaigns", tags=["Campaigns"])
