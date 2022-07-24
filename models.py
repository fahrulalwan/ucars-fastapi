from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    brand_logo = Column(String)
    description = Column(String)


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    brand_id = Column(Integer, ForeignKey("brand.id"))
