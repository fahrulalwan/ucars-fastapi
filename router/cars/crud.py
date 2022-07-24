from fastapi import HTTPException
from sqlalchemy.orm import Session
from router.cars.model import Car as ModelCar

from router.cars import schema


# Cars Queries
def get_cars(db: Session, brand_id: int | None, skip: int = 0, limit: int = 25):
    query = db.query(ModelCar)

    if brand_id is not None and brand_id > 0:
        query = query.filter(ModelCar.brand_id == brand_id)
    else:
        raise HTTPException(status_code=400, detail="Please provide a valid brand id")

    query = query.offset(skip)
    query = query.limit(limit)

    return query.all()


def get_car(db: Session, car_id: int):
    query = db.query(ModelCar)

    query = query.filter(ModelCar.id == car_id)

    return query.first()


def create_car(db: Session, car: schema.CarCreate):
    db_car = ModelCar(
        name=car.name,
        description=car.description,
        brand_id=car.brand_id
    )

    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    return db_car


def update_car(db: Session, car: schema.Car) -> ModelCar:
    query = db.query(ModelCar).get(car.id)

    car.brand_id = query.brand_id

    car_obj = car.dict(exclude_unset=True)

    for key, value in car_obj.items():
        setattr(query, key, value)

    db.add(query)
    db.commit()
    db.refresh(query)

    return query


def delete_car(db: Session, car_id: int):
    query = db.query(ModelCar).get(car_id)

    db.delete(query)
    db.commit()

    return query
