from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


# Brands Queries
def get_brands(db: Session, skip: int = 0, limit: int = 25, keywords: str = ''):
    query = db.query(models.Brand)
    if keywords is not None and len(keywords) > 0:
        query = query.filter(models.Brand.name.ilike('%' + keywords + '%'))

    query = query.offset(skip)
    query = query.limit(limit)

    return query.all()


def get_brand_by_name(db: Session, brand_name: str):
    query = db.query(models.Brand)

    query = query.filter(models.Brand.name == brand_name)

    return query.first()


def get_brand(db: Session, brand_id: int):
    query = db.query(models.Brand)

    query = query.filter(models.Brand.id == brand_id)

    return query.first()


def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(
        brand_logo=brand.brand_logo,
        name=brand.name,
        description=brand.description
    )

    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)

    return db_brand


def update_brand(db: Session, brand: schemas.Brand) -> models.Brand:
    brand_obj = brand.dict(exclude_unset=True)

    query = db.query(models.Brand).get(brand.id)

    for key, value in brand_obj.items():
        setattr(query, key, value)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query


def delete_brand(db: Session, brand_id: int):
    car_query = db.query(models.Car).filter(models.Car.brand_id == brand_id).first()

    if car_query is not None:
        raise HTTPException(status_code=400, detail="Please delete all cars before deleting a brand")

    query = db.query(models.Brand).get(brand_id)

    db.delete(query)
    db.commit()

    return query


# Cars Queries
def get_cars(db: Session, brand_id: int | None, skip: int = 0, limit: int = 25):
    query = db.query(models.Car)

    if brand_id > 0:
        query = query.filter(models.Car.brand_id == brand_id)

    query = query.offset(skip)
    query = query.limit(limit)

    return query.all()


def get_car(db: Session, car_id: int):
    query = db.query(models.Car)

    query = query.filter(models.Car.id == car_id)

    return query.first()


def create_car(db: Session, car: schemas.CarCreate):
    db_car = models.Car(
        name=car.name,
        description=car.description,
        brand_id=car.brand_id
    )

    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    return db_car


def update_car(db: Session, car: schemas.Car) -> models.Car:
    query = db.query(models.Car).get(car.id)

    car.brand_id = query.brand_id

    car_obj = car.dict(exclude_unset=True)

    for key, value in car_obj.items():
        setattr(query, key, value)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query


def delete_car(db: Session, car_id: int):
    query = db.query(models.Car).get(car_id)

    db.delete(query)
    db.commit()

    return query
