from io import BytesIO
import requests
from PIL import Image
import math
import random


def to_ll(ll):
    if type(ll[0]) == float:
        return f"{ll[0]},{ll[1]}"
    else:
        return ll


def from_ll(ll):
    ll = ll.split(",")
    return [float(ll[0]), float(ll[1])]


def get_map_ll(ll, map_type, z=13, pt=None):
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    if pt is not None:
        map_params = {"l": map_type, "ll": to_ll(ll), "z": z, "pt": pt}
    else:
        map_params = {"l": map_type, "ll": to_ll(ll), "z": z}
    response = static_map_request(map_params)
    return Image.open(BytesIO(response.content))


def get_map(name, map_type, z=13):
    ll, spn = get_ll_spn(geocoder_request(name))
    return get_map_from_ll(ll, map_type, z=z)


def search_requests(params):
    api_server = "https://search-maps.yandex.ru/v1/"
    return requests.get(api_server, params=params)


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.0)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def geocoder_request(toponym_to_find, params=None):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    if params is None:
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json",
        }
    else:
        geocoder_params = params
    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response.json()


def get_ll_spn(json_response):
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"
    ]
    lower_x, lower_y = map(
        float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    )
    upper_x, upper_y = map(
        float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()
    )
    toponym_coodrinates = toponym["Point"]["pos"]
    return (
        list(map(float, toponym_coodrinates.split(" "))),
        [str((upper_x - lower_x) / 2), str((upper_y - lower_y) / 2)],
    )


def static_map_request(params):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    return requests.get(map_api_server, params=params)
