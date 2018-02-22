"""
if timezone_str is None:
    print "Could not determine the time zone"
else:
    # Display the current time in that time zone
    timezone = pytz.timezone(timezone_str)
    dt = datetime.datetime.utcnow()
    print "The time in %s is %s" % (timezone_str, dt + timezone.utcoffset(dt))
"""
