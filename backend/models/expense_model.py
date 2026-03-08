from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key = True,index = True)
    category = Column(String(100))
    amount = Column(Float)
    date = Column(Date)
    description = Column(String(250))