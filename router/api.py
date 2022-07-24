from fastapi import APIRouter
from router.brands import controller as brands
from router.cars import controller as cars

api_router = APIRouter()

api_router.include_router(brands.router, prefix="/brands", tags=["Brands"])
api_router.include_router(cars.router, prefix="/cars", tags=["Cars"])
