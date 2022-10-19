from typing import Dict, Union

import requests
from bs4 import BeautifulSoup

import utils


def get_question() -> Union[bool, Dict[str, str]]:
    response = requests.get(utils.TRIVIA_ENDPOINT)
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, 'html.parser')
    question = soup.h2.text
    answer = soup.find('div', {"class": 'answer-text'}).text.split("OR")[
        0].strip()
    return {
        "question": question,
        "answer": answer
    }


def make_quiz_question(question: str, answer: str) -> str:
    question = ("*Question:*\n"
                f"{question}?\n\n"
                f"*Response:*\n"
                f"||{answer}||\n\n").replace("-", "/-").replace(".", "/.")
    credit = f"_Question from [Fun Generators]({utils.TRIVIA_ENDPOINT})_"
    return question + credit
