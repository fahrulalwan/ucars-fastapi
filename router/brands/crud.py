from fastapi import HTTPException
from sqlalchemy.orm import Session
from router.brands.model import Brand as ModelBrand
from router.cars.model import Car as ModelCar

from router.brands import schema


# Brands Queries
def get_brands(db: Session, skip: int = 0, limit: int = 25, keywords: str = ''):
    query = db.query(ModelBrand)
    if keywords is not None and len(keywords) > 0:
        query = query.filter(ModelBrand.name.ilike('%' + keywords + '%'))

    query = query.offset(skip)
    query = query.limit(limit)

    return query.all()


def get_brand_by_name(db: Session, brand_name: str):
    query = db.query(ModelBrand)

    query = query.filter(ModelBrand.name == brand_name)

    return query.first()


def get_brand(db: Session, brand_id: int):
    query = db.query(ModelBrand)

    query = query.filter(ModelBrand.id == brand_id)

    return query.first()


def create_brand(db: Session, brand: schema.BrandCreate):
    db_brand = ModelBrand(
        brand_logo=brand.brand_logo,
        name=brand.name,
        description=brand.description
    )

    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)

    return db_brand


def update_brand(db: Session, brand: schema.Brand) -> ModelBrand:
    brand_obj = brand.dict(exclude_unset=True)

    query = db.query(ModelBrand).get(brand.id)

    for key, value in brand_obj.items():
        setattr(query, key, value)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query


def delete_brand(db: Session, brand_id: int):
    car_query = db.query(ModelCar).filter(ModelCar.brand_id == brand_id).first()

    if car_query is not None:
        raise HTTPException(status_code=400, detail="Please delete all cars before deleting a brand")

    query = db.query(ModelBrand).get(brand_id)

    db.delete(query)
    db.commit()

    return query
