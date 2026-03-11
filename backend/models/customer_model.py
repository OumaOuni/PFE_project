from sqlalchemy import Column, Integer, String, Date
from backend.database import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "luxury"}

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    city = Column(String)
    country = Column(String)
    type = Column(String, default="Regular")
    created_at = Column(Date)
