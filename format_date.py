import os
import datetime
import pytz

remove = [' ', '-', '_', ':', '.']


def get_date_modified(path):
    """fetches the modified date of the file and return it"""
    file_properties = os.stat(path)
    date_modified_timestamp = file_properties.st_mtime
    date_modified = convert_from_timestamp(date_modified_timestamp * 1000)  # get formated the date from TimeStamp fn
    return date_modified


def print_changes(date1, date2, name, data):
    """prints the report"""
    value = modify_date(date1, date2)
    if value:
        print(name)
        print(data)
        print(date1, date2)
        print(date2)
        print()
        return 1


def remove_sp_char(string):
    """Remove extra characters(' ', '-', '_', ':', '.') from the string"""
    for char in remove:
        string = string.replace(char, '')
    return string


def modify_date(date1, date2):
    """Compares the two numbers(date_time) and returns which date is oldest"""
    num1, num2 = remove_sp_char(date1), remove_sp_char(date2)
    num1, num2 = num1[:-2], num2[:-2]
    if num1 == num2:
        return 1
    elif num2 != 'No':  # and num2[8:] != '0000':
        if abs(num1[:8] == num2[:8]) <= 1 or num1 < num2:
            return 1
        else:
            return 0
    return 1


# def change_date(data, modified_date, extracted_date):
#     if modify_date(modified_date, extracted_date):
#         data['date_time'] = modified_date
#         change = True
#     else:
#         data['date_time'] = extracted_date
#         change = False
#     return data, change


def convert_from_timestamp(timestamp):
    """Converts the TImeStamp to date format"""
    if int(timestamp) > 1104537600000:
        timestamp = int(timestamp) / 1000  # Convert milliseconds to seconds

        # Convert the timestamp to a timezone-aware UTC datetime object
        date = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Kolkata'))
        # Return the formatted date
        return date.strftime('%Y-%m-%d %H:%M:%S')

