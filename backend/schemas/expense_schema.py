from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    category : str
    amount : float
    date : date
    description : str