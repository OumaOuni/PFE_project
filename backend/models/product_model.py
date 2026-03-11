from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, ForeignKey
from backend.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "luxury"}

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "luxury"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("luxury.categories.id"))
    collection = Column(String)
    price = Column(Numeric(10, 2))
    cost = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(Date)
