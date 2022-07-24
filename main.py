from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
    openapi_tags=tags_metadata,
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Brand CRUD
@app.post("/brands", response_model=schemas.Brand, tags=['Brands'])
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = crud.get_brand_by_name(db=db, brand_name=brand.name)
    if db_brand:
        raise HTTPException(status_code=400, detail="Brand has already created")
    return crud.create_brand(db, brand)


@app.get("/brands", response_model=list[schemas.Brand], tags=['Brands'])
def read_brands(keywords: str | None = None, skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip, limit, keywords)
    return brands


@app.get("/brands/{brand_id}", response_model=schemas.Brand, tags=['Brands'])
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id not found")
    return db_brand


@app.put("/brands", response_model=schemas.Brand, tags=['Brands'])
def update_brand(brand: schemas.Brand, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id=brand.id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id doesn't exist")
    return crud.update_brand(db, brand)


@app.delete("/brands/{brand_id}", response_model=schemas.Brand, tags=['Brands'])
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id empty")
    return crud.delete_brand(db, brand_id)


# Car CRUD
@app.post("/cars", response_model=schemas.Car, tags=['Cars'])
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)


@app.get("/cars", response_model=list[schemas.Car], tags=['Cars'])
def read_cars(brand_id: int | None = None, skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, brand_id, skip, limit)
    return cars


@app.get("/cars/{car_id}", response_model=schemas.Car, tags=['Cars'])
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id not found")
    return db_car


@app.put("/cars", response_model=schemas.Car, tags=['Cars'])
def update_car(car: schemas.Car, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car.id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id doesn't exist")
    return crud.update_car(db, car)


@app.delete("/cars/{car_id}", response_model=schemas.Car, tags=['Cars'])
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id empty")
    return crud.delete_car(db, car_id)
