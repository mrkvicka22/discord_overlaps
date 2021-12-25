# Gather data about every single user on a server
# - gather mutual servers of each user user_id:{'guilds':{guild_id:"name of guild"}}, 'name':Carrot#3900}
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def setup_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("start-minimized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Firefox(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


if __name__ == '__main__':
    driver = setup_driver("https://discord.com/channels/@me")

