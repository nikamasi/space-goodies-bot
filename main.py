import logging
import re
import sys
from time import sleep

import telebot

import iss
import nasa
import news
import quiz
import utils

bot = telebot.TeleBot(utils.TG_TOKEN)
search_sessions = {}

logging.basicConfig(
    level=logging.ERROR,
    filename="program.log",
    format="%(asctime)s, %(levelname)s, %(message)s, %(name)s"
)

handler = logging.StreamHandler(stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.addHandler(handler)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    search_sessions[message.from_user.id] = False
    bot.send_message(message.chat.id,
                     utils.WELCOME_MESSAGE)
    sleep(2)
    send_instructions(message)


@bot.message_handler(commands=["help"])
def send_instructions(message):
    """Sends a list of available commands."""
    bot.send_message(message.chat.id,
                     utils.DESCRIPTION)


@bot.message_handler(commands=["iss"])
def send_iss_location(message):
    """Requests ISS location data and
    sends the location name with a Google Maps link to the user."""
    try:
        data = iss.get_iss_location()
        if not data:
            bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
            return
        response = utils.ISS_MESSAGE.format(name=data["name"],
                                            link=data["url"])
        bot.send_message(message.chat.id,
                         response,
                         parse_mode=utils.MARKDOWN)
    except Exception as e:
        logger.error(f"Error when handling 'iss' command: "
                     f"{e.__traceback__.tb_next}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)


@bot.message_handler(commands=['pod'])
def send_apod(message):
    """Gets the Picture of the Day and sends it to the user with a caption."""
    try:
        data = nasa.get_picture_of_the_day()
        if not data:
            bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
            return
        header = (f"*{data['title']}*\n"
                  f"_(by {data['author']})_\n")
        description = data['explanation']
        if len(header+description) < utils.CAPTION_LIMIT:
            bot.send_photo(message.chat.id,
                           photo=data["photo"],
                           caption=(header+description),
                           parse_mode=utils.MARKDOWN)
        else:
            bot.send_photo(message.chat.id,
                           photo=data["photo"],
                           caption=header,
                           parse_mode=utils.MARKDOWN)
            if len(description) < utils.MESSAGE_LIMIT:
                bot.send_message(message.chat.id,
                                 description,
                                 parse_mode=utils.MARKDOWN)
    except Exception as e:
        logger.error(f"Error when handling 'pod' command: "
                     f"{e.__traceback__.tb_next}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)


@bot.message_handler(commands=["quiz"])
def send_quiz_question(message):
    """Initiates a quiz search and sends a question
    and a hidden answer to the user."""
    try:
        data = quiz.get_question()
        if not data:
            bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
            return
        response = quiz.make_quiz_question(data["question"], data["answer"])
        bot.send_message(message.chat.id,
                         response,
                         parse_mode=utils.MARKDOWN_V2)
    except Exception as e:
        logger.error(f"Error when handling 'quiz' command: "
                     f"{e.__traceback__.tb_next}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)


def handle_image_search(message):
    """Initiates an image search and sends results to the user."""
    if not re.match(utils.REGEXP, message.text):
        bot.send_message(message.chat.id,
                         utils.ACCEPTED_SYMBOLS_MESSAGE)
        search_sessions[message.from_user.id] = True
        return
    try:
        data = nasa.search_nasa(message.text)
        if not data:
            bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
            search_sessions[message.from_user.id] = False
            return
        bot.send_photo(message.chat.id, data["photo"],
                       caption=f'{data["title"]}, {data["date"]}')
    except Exception as e:
        logger.error(f"Error when handling image search: "
                     f"{e.with_traceback(e.__traceback__)}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
        search_sessions[message.from_user.id] = False


@bot.message_handler(commands=['search'])
def send_search_prompt(message):
    """Prompts the user to send a search query
    and updates user's search session status"""
    try:
        search_sessions[message.chat.id] = True
        bot.send_message(message.chat.id,
                         utils.SEARCH_PROMPT)
    except Exception as e:
        logger.error(f"Error when handling 'search' command: "
                     f"{e.__traceback__.tb_next}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)


@bot.message_handler(commands=['news'])
def send_space_news(message):
    """Initiates a news search and sends a sample of
    5 random articles to the user."""
    try:
        data = news.get_space_news()
        if not data:
            bot.send_message(message.chat.id, utils.ERROR_MESSAGE)
            return
        response = news.make_news_response(data)
        bot.send_message(message.chat.id,
                         response,
                         parse_mode=utils.MARKDOWN)
    except Exception as e:
        logger.error(f"Error when handling 'news' command: "
                     f"{e.__traceback__.tb_next}")
        bot.send_message(message.chat.id, utils.ERROR_MESSAGE)


@bot.message_handler(func=lambda message: True)
def make_command(message):
    """Starts an image search, if user is in a search session.
    Otherwise, sends unknown command message."""
    if message.from_user.id in search_sessions:
        if search_sessions[message.from_user.id]:
            handle_image_search(message)
            return
    else:
        search_sessions[message.from_user.id] = False
    bot.send_message(message.chat.id, utils.UNKNOWN_COMMAND_MESSAGE)


if __name__ == '__main__':
    bot.infinity_polling()
