from datetime import datetime
from random import choice
from typing import Dict, Union

import requests

import utils


def search_nasa(query: str) -> Union[bool, Dict[str, str]]:
    response = requests.get(utils.NASA_SEARCH_ENDPOINT,
                            params={
                                "q": query
                            },
                            headers={
                                "api_key": utils.NASA_API_KEY
                            })
    if response.status_code != 200:
        return False
    items = response.json()['collection']['items']
    item = choice(items)
    title = item["data"][0]["title"]
    try:
        photo = item["links"][0]["href"]
    except KeyError:
        photo = item["href"]
    date_string = item["data"][0]["date_created"]
    new_date_string = datetime.strptime(date_string,
                                        '%Y-%m-%dT%H:%M:%SZ').strftime(
        '%d.%m.%Y')
    return {
        "title": title,
        "photo": photo,
        "date": new_date_string
    }


def get_picture_of_the_day() -> Union[bool, Dict[str, str]]:
    response = requests.get(utils.NASA_APOD_ENDPOINT,
                            params={
                                "api_key": utils.NASA_API_KEY,
                            })
    if response.status_code != 200:
        return False
    response = response.json()
    return {
        "photo": response["url"],
        "title": response["title"],
        "explanation": response["explanation"]
    }
