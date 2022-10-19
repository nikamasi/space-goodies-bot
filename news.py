from datetime import datetime, timedelta
from random import sample
from typing import Union

import requests

import utils


def get_space_news() -> Union[bool, list]:
    date = datetime.now() - timedelta(1)
    res = requests.get(utils.NEWS_ENDPOINT, params={
        "apiKey": utils.NEWS_API_KEY,
        "q": "astronomy",
        "from": date.strftime("%Y-%m-%d"),
        "sortBy": "relevance",
        "language": "en",
        "pageSize": 30,
    })
    if not res:
        return False
    chosen_news = sample(res.json()["articles"], 5)
    return chosen_news


def make_news_response(news: list) -> str:
    response = ""
    for article in news:
        title = article['title'] if article['title'] else ""
        text = (f"*{title}*\n"
                f"{article['description']}\n"
                f"{article['url']}\n\n")
        chars = len(text) + len(response)
        if chars < utils.MESSAGE_LIMIT:
            response += text
        else:
            break
    return response
