# utils.py
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Включаем режим headless
    driver = webdriver.Chrome(service=service, options=options)
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
