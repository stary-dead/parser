# utils.py
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def convert_to_european_size(info):
    us_women_to_eu = {
        "5.5": "35.5",
        "6": "36",
        "6.5": "37",
        "7": "37.5",
        "7.5": "38.5",
        "8": "39",
        "8.5": "40",
        "9": "40.5",
        "9.5": "41",
        "10": "42",
        "10.5": "42.5",
        "11": "43.5",
        "11.5": "44",
        "12": "44.5",
        "12.5": "45",
        "13": "45.5",
        "13.5": "46",
        "14": "47",
        "14.5": "47.5",
        "15": "48",
        "15.5": "49",
        "16": "49.5",
        "16.5": "50"
    }

    us_men_to_eu = {
        "4": "35.5",
        "4.5": "36",
        "5": "37",
        "5.5": "37.5",
        "6": "38",
        "6.5": "39",
        "7": "39.5",
        "7.5": "40",
        "8": "41",
        "8.5": "41.5",
        "9": "42",
        "9.5": "43",
        "10": "43.5",
        "10.5": "44",
        "11": "45",
        "11.5": "45.5",
        "12": "46",
        "12.5": "46.5",
        "13": "47",
        "13.5": "47.5",
        "14": "48",
        "14.5": "48.5",
        "15": "49",
        "15.5": "49.5"
    }

    uk_to_eu = {
        "3.5": "36",
        "4": "36.5",
        "4.5": "37.5",
        "5": "38",
        "5.5": "38.5",
        "6": "39",
        "6.5": "40",
        "7": "40.5",
        "7.5": "41",
        "8": "42",
        "8.5": "42.5",
        "9": "43",
        "9.5": "44",
        "10": "44.5",
        "10.5": "45",
        "11": "45.5",
        "11.5": "46",
        "12": "46.5",
        "12.5": "47",
        "13": "47.5",
        "14": "48",
        "14.5": "48.5"
    }

    has_price = False
    for item in info:
        size = item["size"]
        price = item["price"]
        if (price != "$--") and (price != None) and (price != ""):
            has_price = True
        else:
            item["price"] = ""
        if size.startswith("US W"):
            us_size = size.split()[2]
            if us_size[-1] in ("Y", "C", "W", "N"):
                us_size = us_size[:-1]  # Удаляем последнюю букву
            if us_size in us_women_to_eu:
                item["size"] = us_women_to_eu[us_size]
        elif size.startswith("US M"):
            us_size = size.split()[2]
            if us_size[-1] in ("Y", "C", "W", "N"):
                us_size = us_size[:-1]  # Удаляем последнюю букву
            if us_size in us_men_to_eu:
                item["size"] = us_men_to_eu[us_size]
        elif size.startswith("UK"):
            uk_size = size.split()[1]
            if uk_size[-1] in ("Y", "C", "W", "N"):
                uk_size = uk_size[:-1]  # Удаляем последнюю букву
            if uk_size in uk_to_eu:
                item["size"] = uk_to_eu[uk_size]

    return info, has_price

def calculate_execution_time(start_time):
    end_time = time.time()
    return end_time - start_time

def get_splited_urls(driver_count, urls):
    num_drivers = [[] for _ in range(driver_count)]

    for index, url in enumerate(urls):
        num_driver_index = index % driver_count
        num_drivers[num_driver_index].append(url)
    return num_drivers

def fetch_page_content(driver, url):
    driver.get(url)
    return driver.page_source

async def fetch_page_content_async(driver, url):
    await driver.get(url)
    return driver.page_source

async def close_modal_async(driver):
    try:
        modal_close_button = await WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-modal-close'))
        )
        await modal_close_button.click()
    except:
        pass
def close_modal(driver):
    try:
        modal_close_button = driver.find_element(By.CLASS_NAME, 'ant-modal-close')
        if modal_close_button:
            modal_close_button.click()
    except Exception as e:
        print("Нет всплывающего баннера")
        
def initialize_webdriver(base_url):
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')  # Включаем режим headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(base_url)
    return driver

def click_next_page(driver):
    next_button = None
    try:
        next_button = driver.find_element(By.XPATH, '//li[@class="ant-pagination-next"]/button')
    except NoSuchElementException:
        print("Ошибка. Нет такой кнопки")
        return False
    
    if next_button and next_button.is_displayed():
        next_button.click()
        return True
    else:
        return False
