# Gather data about every single user on a server
# - gather mutual servers of each user user_id:{'guilds':{guild_id:"name of guild"}}, 'name':Carrot#3900}
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time


def setup_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("start-minimized")
    options.add_argument("disable-infobars")
    #options.add_experimental_option('w3c', False)
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


def login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes("https://discord.com/login?redirect_to=%2Fchannels%2F%40me"))
    wait.until(EC.url_changes("https://discord.com/channels/@me"))
    return driver


def get_server_list(soup):
    elements = soup.find_all('div', {'class': 'wrapper-1BJsBx'})
    return {ele['href'] for ele in elements[1:]}  # get all the urls to servers and ignore @me server


def get_users(soup, driver, user_set):
    last_l = len(user_set)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    wait = WebDriverWait(driver, 3)
    elements = driver.find_elements_by_class_name('wrapper-3t9DeA')
    for ele in elements:
        user_set.add(ele.get_attribute('aria-label').split(',')[0])

    while len(user_set) > last_l:
        last_l = len(user_set)
        wait.until(EC.element_to_be_clickable(elements[-1]))
        elements[-1].click()
        elements = driver.find_elements_by_class_name('wrapper-3t9DeA')
        for ele in elements:
            user_set.add(ele.get_attribute('aria-label').split(',')[0])
    print(user_set)



    #print([ele['aria-label'].split(',')[0] for ele in elements[1:]])

    #TouchActions(driver).scroll_from_element(elements[-1], yoffset=30*len(elements), xoffset=0).perform()

if __name__ == '__main__':
    driver = setup_driver("https://discord.com/channels/@me")
    driver = login(driver)
    time.sleep(3)
    source = driver.page_source
    user_set = set()
    soup = BeautifulSoup(source, "html.parser")
    server_list = get_server_list(soup)
    for server_href in server_list:
        driver.get("https://discord.com" + server_href)
        time.sleep(10)
        server_source = driver.page_source
        server_soup = BeautifulSoup(server_source, "html.parser")
        get_users(server_soup, driver, user_set)
