from fastapi import FastAPI
from config.database import SessionLocal, engine
from router.api import api_router
from router.brands import model as brands_model
from router.cars import model as cars_model

brands_model.Base.metadata.create_all(bind=engine)
cars_model.Base.metadata.create_all(bind=engine)

description = """
UCARS Backend API
"""

tags_metadata = [
    {
        "name": "Brands",
        "description": "Operations with Brand management.",
    },
    {
        "name": "Cars",
        "description": "Manage Car items inside **Brands**.",
    }
]

contact_metadata = {
    "name": "Mohammad Fahrul Alwan",
    "url": "https://fahrulalwan.vercel.app",
    "email": "fahrulalwan@gmail.com"
}

app = FastAPI(
    title='UCARS Backend',
    description=description,
    version='1.0.0',
    openapi_tags=tags_metadata
)


app.include_router(api_router)
