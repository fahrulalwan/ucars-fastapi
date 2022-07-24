from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from router.cars import crud, schema
from config.session import get_db

router = APIRouter()


@router.post("", response_model=schema.Car)
def create_car(car: schema.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)


@router.get("", response_model=list[schema.Car])
def read_cars(brand_id: int | None = None, skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, brand_id, skip, limit)
    return cars


@router.get("/{car_id}", response_model=schema.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id not found")
    return db_car


@router.put("", response_model=schema.Car)
def update_car(car: schema.Car, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car.id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id doesn't exist")
    return crud.update_car(db, car)


@router.delete("/{car_id}", response_model=schema.Car)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car id empty")
    return crud.delete_car(db, car_id)
