from pydantic import BaseModel
from sqlalchemy.orm import validates


# Car Schemas
class CarBase(BaseModel):
    name: str
    description: str | None = None
    brand_id: int

    @validates('brand_id')
    def validates_brand_id(self, key, value):
        if self.brand_id and self.brand_id != value:  # Field already exists
            raise ValueError('brand_id cannot be modified.')
        return value


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

    @validates('id')
    def validates_brand_id(self, key, value):
        if self.id and self.id != value:  # Field already exists
            raise ValueError('id cannot be modified.')
        return value
