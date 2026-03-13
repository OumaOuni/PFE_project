from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean
from backend.database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "openrational"}

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200))
    category_id = Column(Integer)
    cost_price = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2))
    creation_date = Column(Date)
    is_active = Column(Boolean, default=True)
