from geo import TIMEZONE_FINDER


def get_timezone(lng, lat):
    """
    Returns the Time Zone by coordinates

    :param float lng: longitude
    :param float lat: latitude
    :return: the timezone name
    """
    tf = TIMEZONE_FINDER
    timezone_str = tf.certain_timezone_at(lng=lng, lat=lat)

    if timezone_str is None:
        timezone_str = tf.closest_timezone_at(lng=lng, lat=lat)

    if timezone_str is None:
        timezone_str = tf.closest_timezone_at(lng=lng, lat=lat, delta_degree=3)

    if isinstance(timezone_str, (tuple,)):
        timezone_str = timezone_str[0]

    return timezone_str
