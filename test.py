from datetime import timedelta, datetime

delta = timedelta(days=90)
print(delta.month())
today = datetime.today()
mydate = today + delta
print(mydate.month)
