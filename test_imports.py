#!/usr/bin/env python
"""Simple test to check imports without starting the server"""

try:
    print("Testing database import...")
    from backend.database import engine, Base, SessionLocal
    print("✓ Database imported successfully")
    
    print("\nTesting models...")
    from backend.models.user_model import User
    print("✓ User model imported")
    
    from backend.models.expense_model import Expense
    print("✓ Expense model imported")
    
    print("\nTesting schemas...")
    from backend.schemas.user_schema import UserCreate, UserResponse
    print("✓ User schema imported")
    
    from backend.schemas.expense_schema import ExpenseCreate
    print("✓ Expense schema imported")
    
    print("\nTesting routes...")
    from backend.routes.user_routes import router as user_router
    print("✓ User routes imported")
    
    from backend.routes.expense_routes import router as expense_router
    print("✓ Expense routes imported")
    
    print("\nTesting FastAPI app...")
    from backend.main import app
    print("✓ FastAPI app imported successfully!")
    
    print("\n✓ ALL TESTS PASSED!")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERROR: {e}")
    traceback.print_exc()
