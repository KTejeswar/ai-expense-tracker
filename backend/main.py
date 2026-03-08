from fastapi import FastAPI
from backend.database import engine, Base
from backend.models.expense_model import Expense
from backend.models.user_model import User
from backend.routes.expense_routes import router as expense_router
from backend.routes.user_routes import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(expense_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker Backend Running"}
