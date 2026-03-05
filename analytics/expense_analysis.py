import pandas as pd

def calculate_total(expenses):
    df=pd.DataFrame(expenses)
    return df['amount'].sum()

def category_summary(expenses):
    df = pd.DataFrame(expenses)
    # normalize category strings (strip + title-case) so grouping is consistent and display-friendly
    if 'category' in df.columns:
        df['category'] = df['category'].astype(str).str.strip().str.title()
    return df.groupby("category")["amount"].sum().to_dict()