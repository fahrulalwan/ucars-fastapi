from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from router.brands import crud, schema
from config.session import get_db

router = APIRouter()


@router.post("", response_model=schema.Brand)
def create_brand(brand: schema.BrandCreate, db: Session = Depends(get_db)):
    db_brand = crud.get_brand_by_name(db=db, brand_name=brand.name)
    if db_brand:
        raise HTTPException(status_code=400, detail="Brand has already created")
    return crud.create_brand(db, brand)


@router.get("", response_model=list[schema.Brand])
def read_brands(keywords: str | None = None, skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip, limit, keywords)
    return brands


@router.get("/{brand_id}", response_model=schema.Brand)
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id not found")
    return db_brand


@router.put("", response_model=schema.Brand)
def update_brand(brand: schema.Brand, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id=brand.id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id doesn't exist")
    return crud.update_brand(db, brand)


@router.delete("/{brand_id}", response_model=schema.Brand)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand id empty")
    return crud.delete_brand(db, brand_id)
