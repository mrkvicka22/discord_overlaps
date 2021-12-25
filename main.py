# Gather data about every single user on a server
# - gather mutual servers of each user user_id:{'guilds':{guild_id:"name of guild"}}, 'name':Carrot#3900}
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("start-minimized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


def login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes("https://discord.com/login?redirect_to=%2Fchannels%2F%40me"))
    wait.until(EC.url_changes("https://discord.com/channels/@me"))
    return driver

def server_list(soup):
    elements = soup.find_all('div', {'class': 'wrapper-1BJsBx'})
    return {ele['href'] for ele in elements[1:]} # get all the urls to servers and ignore @me server

if __name__ == '__main__':
    driver = setup_driver("https://discord.com/channels/@me")
    driver = login(driver)
    time.sleep(3)
    source = driver.page_source
    print(source)

    soup = BeautifulSoup(source, "html.parser")
    server_list = server_list(soup)


