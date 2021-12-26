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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
import time


def setup_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("start-minimized")
    options.add_argument("disable-infobars")
    # options.add_experimental_option('w3c', False)
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


def login(driver):
    wait = WebDriverWait(driver, 30)
    wait.until(EC.url_changes("https://discord.com/login?redirect_to=%2Fchannels%2F%40me"))
    wait.until(EC.url_changes("https://discord.com/channels/@me"))
    return driver


def get_server_list(soup):
    elements = soup.find_all('div', {'class': 'wrapper-1BJsBx'})
    return {(ele['href'], ele['aria-label']) for ele in
            elements[1:]}  # get all the urls to servers and ignore @me server


def get_users(soup, driver, user_set, guild):
    def get_data(elem, click_elem):
        for ele, cele in zip(elem, click_elem):
            try:
                # src="https://cdn.discordapp.com/avatars/223178858369777664/deb634eaec34453bd8aa5a2b90086b09.webp?size=40"
                user_id = (ele.get_attribute('src').split('/')[4])
                user_name = cele.get_attribute('aria-label').split(",")[0]
                if user_id not in user_set:
                    user_set[user_id] = {'guilds': dict(), 'name': user_name}
                user_set[user_id]["guilds"][guild[0]] = guild[1]

            except StaleElementReferenceException:
                print(ele)
                pass

    last_l = len(user_set)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    wait = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)
    elements = driver.find_elements_by_class_name('avatar-VxgULZ')
    clickable_elements = driver.find_elements_by_class_name('wrapper-3t9DeA')
    print(len(elements), elements)

    get_data(elements, clickable_elements)
    while len(user_set) > last_l:
        last_l = len(user_set)
        wait.until(EC.element_to_be_clickable(clickable_elements[-1]))
        try:
            clickable_elements[-1].click()
        except ElementClickInterceptedException:
            clickable_elements = driver.find_elements_by_class_name('wrapper-3t9DeA')
            clickable_elements[-1].click()
        elements = driver.find_elements_by_class_name('avatar-VxgULZ')
        clickable_elements = driver.find_elements_by_class_name('wrapper-3t9DeA')
        get_data(elements, clickable_elements)
    return user_set

    # print([ele['aria-label'].split(',')[0] for ele in elements[1:]])

    # TouchActions(driver).scroll_from_element(elements[-1], yoffset=30*len(elements), xoffset=0).perform()


if __name__ == '__main__':
    driver = setup_driver("https://discord.com/channels/@me")
    driver = login(driver)
    time.sleep(3)
    source = driver.page_source
    user_set = dict()
    soup = BeautifulSoup(source, "html.parser")
    server_list = get_server_list(soup)
    data = []
    for server_href, server_name in server_list:
        driver.get("https://discord.com" + server_href)
        time.sleep(10)
        server_source = driver.page_source
        server_soup = BeautifulSoup(server_source, "html.parser")
        guild = server_soup.find('')
        user_set = get_users(server_soup, driver, user_set, (server_href.split("/")[2], server_name))
