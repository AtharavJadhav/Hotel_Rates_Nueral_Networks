import pandas as pd
from datetime import datetime, timedelta
import holidays
from datetime import date
from hijri_converter import convert

# Load the CSV file
file_path = "C:/Users/Atharav Jadhav/Desktop/VSCODE FILES/Python/Calendar/Test_Data.csv"
df = pd.read_csv(file_path)

# Function to parse the date
def parse_date(date_str):
    return datetime.strptime(date_str, "%d-%m-%y").date()

##################### Catageorizing the Season ########################
# Function to categorize the season
def categorize_season(row):
    return get_season(row['CHECKIN'].month)
# Function to get the season for a given month
def get_season(month):
    if month in [11, 12, 1, 2]:  # Winter
        return 'Winter'
    elif month in [3, 4, 5, 6]:  # Summer
        return 'Summer'
    elif month in [7, 8, 9, 10]:  # Monsoon
        return 'Monsoon'
    else:  # Autumn
        return 'Autumn'
#######################################################################

##################### WEEK NUMBER CATAGEORIZATION #####################
# Function to get the week number for a given date
def get_week_number(date):
    return date.isocalendar()[1]
# Function to categorize the week number
def categorize_week(row):
    return get_week_number(row['CHECKIN'])
#######################################################################

############################# HOLIDAYS ################################
# Function to check if a given date is a holiday
def is_holiday(year, month, day):
    # New Year's Day
    if month == 1 and day == 1:
        return True, 'New Years Day'

    # Republic Day (January 26th)
    if month == 1 and day == 26:
        return True, 'Republic Day'

    # Independence Day (August 15th)
    if month == 8 and day == 15:
        return True, 'Independence Day'

    # Gandhi Jayanti (October 2nd)
    if month == 10 and day == 2:
        return True, 'Gandhi Jayanti'

    # Christmas Day (December 25th)
    if month == 12 and day == 25:
        return True, 'Christmas Day'

    # Diwali (variable date)
    if month == calculate_diwali_month(year) and day == calculate_diwali_date(year):
        return True, 'Diwali'

    # Eid (variable date)
    if month == calculate_eid_month(year) and day == calculate_eid_date(year):
        return True, 'Eid'
    
    # Ganesh Chaturthi (variable date)
    if month == calculate_ganesh_chaturthi_month(year) and day == calculate_ganesh_chaturthi_date(year):
        return True, 'Ganesh Chaturthi'
    
    # Holi (variable date)
    if month == calculate_holi_month(year) and day == calculate_holi_date(year):
        return True, 'Holi'

    # Add more holidays as needed...

    return False

def calculate_diwali_date(year):
    diwali_date = convert.Gregorian(year, 7, 15).to_hijri().day
    return diwali_date
def calculate_diwali_month(year):
    diwali_month = convert.Gregorian(year, 7, 15).to_hijri().month
    return diwali_month

def calculate_ganesh_chaturthi_date(year):
    ganesh_chaturthi_date = convert.Gregorian(year, 5, 4).to_hijri().day
    return ganesh_chaturthi_date
def calculate_ganesh_chaturthi_month(year):
    ganesh_chaturthi_month = convert.Gregorian(year, 5, 4).to_hijri().month
    return ganesh_chaturthi_month

def calculate_holi_date(year):
    holi_date = convert.Gregorian(year, 1, 15).to_hijri().day
    return holi_date
def calculate_holi_month(year):
    holi_month = convert.Gregorian(year, 1, 15).to_hijri().month
    return holi_month

def calculate_eid_month(year):
    eid_month = convert.Gregorian(year, 10, 1).to_hijri().month
    return eid_month
def calculate_eid_date(year):
    eid_date = convert.Gregorian(year, 10, 1).to_hijri().day
    return eid_date

# Get holidays for a specific year
def get_india_holidays(year):
    holidays = []
    for month in range(1, 13):
        for day in range(1, 32):
            if is_holiday(year, month, day):
                holidays.append(date(year, month, day))
    return holidays
# Function to get the name of the holiday for a given date
def get_holiday_name(date):
    year = date.year
    month = date.month
    day = date.day

    if is_holiday(year, month, day)[0]:
        return is_holiday(year, month, day)[1]

    return 'Unknown Holiday'
#######################################################################

# Function to categorize the type (holiday, weekend, or weekday)
def categorize_type(row):
    checkin = row['CHECKIN']
    checkout = row['CHECKOUT']
    has_holiday = False

    for date in pd.date_range(start=checkin, end=checkout):
        if date.date() in india_holidays:  # Holiday
            has_holiday = True
            holiday_date = date.date()
            holiday_name = get_holiday_name(holiday_date)
            break  # Exit the loop once a holiday is found

    if has_holiday:
        return 'Holiday: ' + holiday_name
    elif any(date.weekday() in [5, 6] for date in pd.date_range(start=checkin, end=checkout)):
        return 'Weekend'
    else:
        return 'Weekday'

########################## Long WEEKENDS ##############################
def is_long_weekend(checkin, checkout):
    # Initialize flags
    holiday_flag = False
    saturday_flag = False
    sunday_flag = False

    # Check if there is at least one holiday, one Sunday, and one Saturday between CHECKIN and CHECKOUT
    for date in pd.date_range(start=checkin, end=checkout):
        if date.date() in india_holidays:  # Check for holiday
            holiday_flag = True
        if date.weekday() == 6:  # Check for Sunday
            sunday_flag = True
        if date.weekday() == 5:  # Check for Saturday
            saturday_flag = True

    return int(holiday_flag and sunday_flag and saturday_flag)
#######################################################################

######################### Long Holidays ###############################
def is_long_holiday(checkin, checkout):
    holidays = pd.date_range(start=checkin, end=checkout, inclusive='left')
    num_holidays = len([date for date in holidays if date.date() in india_holidays])
    if num_holidays >= 3:
        return 1
    elif num_holidays >= 1 and is_long_weekend(checkin, checkout) == 1:
        return 1
    else:
        return 0
#######################################################################

df['CHECKIN'] = df['CHECKIN'].apply(parse_date)
df['CHECKOUT'] = df['CHECKOUT'].apply(parse_date)
df['SEASON'] = df.apply(categorize_season, axis=1)
df['WEEK'] = df.apply(categorize_week, axis=1)
# Get unique years from the CHECKIN column
years = df['CHECKIN'].apply(lambda x: x.year).unique()
# Create an empty list to store the India holidays for all years
india_holidays = []
# Iterate over each year and get the holidays
for year in years:
    india_holidays.extend(get_india_holidays(year))
# Apply the categorize_type function to create the TYPE column
df['TYPE'] = df.apply(categorize_type, axis=1)
df['LONG WEEKEND'] = df.apply(lambda row: is_long_weekend(row['CHECKIN'], row['CHECKOUT']), axis=1)
df['LONG HOLIDAY'] = df.apply(lambda row: is_long_holiday(row['CHECKIN'], row['CHECKOUT']), axis=1)


# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)

print("Date types (holiday name, weekend, season, week number, and long holidays) have been added to the CSV file.")