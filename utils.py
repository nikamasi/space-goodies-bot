from os import getenv

""" BOT MESSAGE TEMPLATES """
ERROR_MESSAGE = "Houston, we have a problem! ⚠️ Please try this later!"
MENU_MESSAGE = ("Choose what you want to do using the menu "
                "or type commands directly.")
UNKNOWN_COMMAND_MESSAGE = "Can't help you, but I tried 🤷🏻‍♀️"
WELCOME_MESSAGE = ("✨✨✨✨✨\n"
                   "Your Space Goodies Bot is ready to expand your horizons!\n"
                   f"{MENU_MESSAGE}")
SEARCH_PROMPT = "Please enter a query for the search (English only)"
DESCRIPTION = ("Here's what you can do:\n"
               "- /search - search NASA images database 🪐\n"
               "- /news - get the latest astro news 📰\n"
               "- /iss - get the current location of ISS 👩‍🚀\n"
               "- /pod - get NASA's Picture of the Day 🌃\n"
               "- /quiz - get a Space Quiz question 🌚")
ISS_MESSAGE = "ISS is flying over [{name}]({link}) now."
ACCEPTED_SYMBOLS_MESSAGE = ("I accept only latin letters, numbers, "
                            "underscores and dashes")

"""API KEYS """
TG_TOKEN = getenv('TG_TOKEN')
NASA_API_KEY = getenv('NASA_API_KEY')
GEOAPIFY_API_KEY = getenv("GEOAPIFY_API_KEY")
NEWS_API_KEY = getenv('NEWS_API_KEY')

"""ENDPOINTS"""
TRIVIA_ENDPOINT = "https://fungenerators.com/random/trivia/Space"
NASA_APOD_ENDPOINT = f'https://api.nasa.gov/planetary/apod'
NASA_SEARCH_ENDPOINT = 'https://images-api.nasa.gov/search?'
NEWS_ENDPOINT = f"https://newsapi.org/v2/everything"
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"
GOOGLE_MAPS_ENDPOINT = ("http://www.google.com/maps/"
                        "place/{latitude},{longitude}")
GEOAPIFY_ENDPOINT = "https://api.geoapify.com/v1/geocode/reverse"

""" OTHER """
CAPTION_LIMIT = 1024
MESSAGE_LIMIT = 4096

MARKDOWN = "Markdown"
MARKDOWN_V2 = "MarkdownV2"

REGEXP = "^[A-Za-z 0-9_-]*$"
