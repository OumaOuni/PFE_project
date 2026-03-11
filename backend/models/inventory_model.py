from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {"schema": "luxury"}

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("luxury.products.id"), unique=True)
    quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=5)
    reorder_point = Column(Integer, default=10)
    last_updated = Column(DateTime, server_default=func.now())
