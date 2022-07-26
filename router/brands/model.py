from sqlalchemy import Column, Integer, String

from config.database import Base


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    brand_logo = Column(String)
    description = Column(String)
