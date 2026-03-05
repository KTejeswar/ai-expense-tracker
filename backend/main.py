import sys
from pathlib import Path

# Ensure project root is on sys.path so sibling packages (like `analytics`) are importable
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from database import engine,Base
from models.expense_model import Expense
from routes.expense_routes import router as expense_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(expense_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker Backend Running"}
