from pydantic import BaseModel
from sqlalchemy.orm import validates


# Brand Schemas
class BrandBase(BaseModel):
    name: str
    brand_logo: str | None = None
    description: str | None = None


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int

    class Config:
        orm_mode = True

    @validates('id')
    def validates_brand_id(self, key, value):
        if self.id and self.id != value:  # Field already exists
            raise ValueError('id cannot be modified.')
        return value
