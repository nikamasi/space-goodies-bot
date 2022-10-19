# Space Goodies Bot
A Telegram bot for getting space related information.


## Supported commands:
* /search - search NASA images database 🪐
* /news - get the latest astro news 📰
* /iss - get the current location of ISS 👩‍🚀
* /pod - get NASA's Picture of the Day 🌃
* /quiz - get a Space Quiz question 🌚

## Technologies:
* bot managed with [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* some information scraped using [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)


Public REST APIs or endpoints that bot accesses:
- [NASA APIs](https://api.nasa.gov) - Astronomy Picture of the Day, NASA Image and Video Library
- [ISS Current Location API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/) - current latitude and longitude of the ISS
- [FunGenerators](https://fungenerators.com/random/trivia/Space) - space themed Trivia questions
- [NewsAPI](https://newsapi.org) - getting the latest astronomy news
- [Reverse Geocoding API](https://www.geoapify.com/reverse-geocoding-api) - converts lat/long coordinates to a location address

