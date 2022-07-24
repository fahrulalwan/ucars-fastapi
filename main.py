from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
