from datetime import datetime
import pytz
from tzlocal import get_localzone  # Make sure to install tzlocal package

# Get the local time
local_time = datetime.now()
print("Local time:", local_time)

#get the UTC time
utc_time = datetime.utcnow()
print("UTC time:", utc_time)

# find out if we should add or subtract the time difference
if local_time > utc_time:
    print("Local time is ahead of UTC time")
    print("here")
    time_difference = local_time - utc_time
else:
    print("Local time is behind UTC time")
    time_difference = utc_time - local_time
    print("here2")
print("Time difference:", time_difference)
print((time_difference))