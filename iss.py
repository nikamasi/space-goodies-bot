from typing import Dict, Union

import requests

import utils


def get_iss_location() -> Union[bool, Dict[str, str]]:
    response = requests.get(utils.ISS_ENDPOINT)
    if response.status_code != 200:
        return False
    iss_position = response.json()["iss_position"]
    maps_url = utils.GOOGLE_MAPS_ENDPOINT.format(
        latitude=iss_position["latitude"],
        longitude=iss_position["longitude"])
    name = get_location_name(iss_position["latitude"],
                             iss_position["longitude"])
    return {
        "url": maps_url,
        "name": name
    }


def get_location_name(lat: str, lon: str) -> str:
    try:
        response = requests.get(utils.GEOAPIFY_ENDPOINT,
                                params={
                                    "lat": lat,
                                    "lon": lon,
                                    "apiKey": utils.GEOAPIFY_API_KEY
                                })
        name = (response.json()["features"][0]["properties"]["address_line1"] +
                response.json()["features"][0]["properties"]["address_line2"])
    except requests.RequestException or KeyError:
        name = "here"
    return name
