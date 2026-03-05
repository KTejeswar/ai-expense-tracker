from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import SessionLocal
from models.expense_model import Expense
from schemas.expense_schema import ExpenseCreate

router = APIRouter()


def validate_expense_payload(payload: ExpenseCreate):
    # Ensure required fields are present and not null/empty
    if payload.category is None or (isinstance(payload.category, str) and payload.category.strip() == ""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`category` is required and cannot be empty")
    if payload.amount is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`amount` is required and cannot be null")
    if payload.date is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`date` is required and cannot be null")
    if payload.description is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`description` is required and cannot be null")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@router.post("/add-expense")
def add_expense(expense : ExpenseCreate, db : Session = Depends(get_db)):
    # validate incoming payload
    validate_expense_payload(expense)
    new_expense = Expense(
        category = expense.category.strip().lower(),
        amount = expense.amount,
        date = expense.date,
        description = expense.description
    )
    try:
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message" : "Expense added successfully"}

@router.get("/expenses")
def get_expenses(db : Session = Depends(get_db)):
    try:
        expenses = db.query(Expense).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    result = []
    for e in expenses:
        result.append({
            "id": e.id,
            "category": e.category,
            "amount": e.amount,
            "date": str(e.date),
            "description": e.description,
        })
    return result

@router.delete("/delete-expense/{expense_id}")
def delete_expense(expense_id : int,db : Session = Depends(get_db)):
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    try:
        db.delete(expense)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message" : "Expense deleted Successfully"}

@router.put("/update-expense/{expense_id}")
def update_expense(expense_id : int, updated_data : ExpenseCreate,db : Session = Depends(get_db)):
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not Found")

    # validate incoming payload
    validate_expense_payload(updated_data)

    expense.category = updated_data.category.strip().lower() if isinstance(updated_data.category, str) else updated_data.category
    expense.amount = updated_data.amount
    expense.date = updated_data.date
    expense.description = updated_data.description

    try:
        db.commit()
        db.refresh(expense)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message" : "Expense Updated Successfully"}

@router.get("/expense-summary")
def expense_summary(db : Session = Depends(get_db)):
    try:
        expenses = db.query(Expense).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    expenses_list = [
        {
            "category": e.category,
            "amount": e.amount,
            "date": e.date,
            "description": e.description,
        }
        for e in expenses
    ]

    try:
        from analytics.expense_analysis import calculate_total, category_summary
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analytics import error: {e}")

    try:
        total = calculate_total(expenses_list)
        summary = category_summary(expenses_list)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analytics calculation error: {e}")

    return {"total": total, "category_summary": summary}