# Reference: https://www.geeksforgeeks.org/program-distance-two-points-earth/
# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, sqrt

from address_book import logger


def get_distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    distance = (c * r)
    logger.debug(
        f'Distance between latitude-1 {lat1}, longitude-1 {lon1} and latitude-2 {lat2}, longitude-2 {lon2} is {distance} KM')
    return distance
