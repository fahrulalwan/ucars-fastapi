from sqlalchemy import Column, ForeignKey, Integer, String
from config.database import Base


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    brand_id = Column(Integer, ForeignKey("brand.id"))
