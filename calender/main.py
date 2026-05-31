import datetime
# import persian 
# import jalali

# Define a function to convert from Miladi to Shamsi
def miladi_to_shamsi(miladi_date):
    shamsi_year = miladi_date.year - 622
    shamsi_month = miladi_date.month + 9
    shamsi_day = miladi_date.day + 8
    return datetime.datetime(shamsi_year, shamsi_month, shamsi_day)

# Test the functions
miladi_date = datetime.datetime.now()
shamsi_date =miladi_to_shamsi(miladi_date)
print("Shamsi date:", shamsi_date.date())
print("Shamsi date:", shamsi_date.ctime())
print("Shamsi date:", shamsi_date.weekday())
print()
print("Miladi date:", miladi_date.date())
print("Miladi date:", miladi_date.ctime())

