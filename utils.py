from datetime import date

def get_date():
    today_date = date.today()
    today_date = today_date.strftime("%Y-%m-%d")
    return f"{today_date}.csv"
