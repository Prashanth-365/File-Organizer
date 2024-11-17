import datetime
import pytz

# The timestamp from the image file name
timestamp = 1556187466849 / 1000  # Convert milliseconds to seconds

# Create a timezone for Indian Standard Time
ist = pytz.timezone('Asia/Kolkata')

# Convert the timestamp to a timezone-aware UTC datetime object
date_utc = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

# Convert UTC to IST
date_ist = date_utc.astimezone(ist)

# Print the formatted date in IST
print("IST:", date_ist.strftime('%Y-%m-%d %H:%M:%S'))
