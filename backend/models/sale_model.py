from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from backend.database import Base


class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {"schema": "luxury"}

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("luxury.products.id"))
    customer_id = Column(Integer, ForeignKey("luxury.customers.id"))
    salesperson_id = Column(Integer, ForeignKey("luxury.salespersons.id"))
    quantity = Column(Integer)
    unit_price = Column(Numeric(10, 2))
    total_amount = Column(Numeric(10, 2))
    sale_date = Column(Date)
    region = Column(String)
    city = Column(String)
    status = Column(String, default="completed")
