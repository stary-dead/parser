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

import re
default_table = [    ["US Men", "US Women", "EU", "UK"],
    ["3.5", "5", "35.5", "3"],
    ["4", "5.5", "36", "3.5"],
    ["4.5", "6", "36.5", "4"],
    ["5", "6.5", "37.5", "4.5"],
    ["5.5", "7", "38", "5"],
    ["6", "7.5", "38.5", "5.5"],
    ["6.5", "8", "39", "6"],
    ["7", "8.5", "40", "6"],
    ["7.5", "9", "40.5", "6.5"],
    ["8", "9.5", "41", "7"],
    ["8.5", "10", "42", "7.5"],
    ["9", "10.5", "42.5", "8"],
    ["9.5", "11", "43", "8.5"],
    ["10", "11.5", "44", "9"],
    ["10.5", "12", "44.5", "9.5"],
    ["11", "12.5", "45", "10"],
    ["11.5", "13", "45.5", "10.5"],
    ["12", "13.5", "46", "11"],
    ["12.5", "14", "47", "11.5"],
    ["13", "14.5", "47.5", "12"],
    ["13.5", "15", "48", "12.5"],
    ["14", "15.5", "48.5", "13"],
    ["14.5", "16", "49", "13.5"],
    ["15", "16.5", "49.5", "14"],
    ["15.5", "17", "50", "14.5"],
    ["16", "17.5", "50.5", "15"],
    ["16.5", "18", "51", "15.5"],
    ["17", "18.5", "51.5", "16"],
    ["17.5", "19", "52", "16.5"],
    ["18", "19.5", "52.5", "17"],
    ["18.5", "20", "53", "17.5"],
    ["19", "20.5", "53.5", "18"],
    ["19.5", "21", "54", "18.5"],
    ["20", "21.5", "54.5", "19"],
    ["20.5", "22", "55", "19.5"],
    ["21", "22.5", "55.5", "20"],
    ["21.5", "23", "56", "20.5"],
    ["22", "23.5", "56.5", "21"]
]

def parse_size_string(size_string, table):
    format_pattern = r'(?P<format>US|UK|US)'
    gender_pattern = r'(?P<gender>[MW]?)' 
    category_pattern = r'(Kids)?'
    size_pattern = r'(?P<size>\d+(\.\d+)?)'
    age_pattern = r'(?P<age>[YCY]?)'

    pattern = fr'{format_pattern}\s*{gender_pattern}\s*{category_pattern}\s*{size_pattern}\s*{age_pattern}'
    parsed_data = []
    matches = re.finditer(pattern, size_string)

    for match in matches:
        data_dict = match.groupdict()

        if not data_dict['gender']:
            data_dict['gender'] = 'Unisex'

        if data_dict['size']:
            data_dict['size'] = float(data_dict['size'])
        
        if not data_dict['age']:
            data_dict['age'] = None

        data_dict['eu_size'] = find_eu_value(table, data_dict['size'])
        
        parsed_data.append(data_dict)

    return parsed_data

def format_size(info, table):
    has_price = False
    if len(table) == 0:
        table = default_table
    for item in info:
        size = item["size"]
        item["formatted_size"] = parse_size_string(size, table)
        price = item["price"]
        if (price != "$--") and (price != None) and (price != ""):
            has_price = True
        else:
            item["price"] = ""
        

    return info, has_price

def find_eu_value(table, target_size):
    formatted_target_size = remove_decimal_zero(str(target_size))
    eu_index = table[0].index("EU")   
    for row in table[1:]:
        if row[0] == "/":
            continue
        
        if formatted_target_size in row[0]:
            return row[eu_index]  
    return None

def remove_decimal_zero(string):
    if string.endswith(".0"):
        return string[:-2]
    return string

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
        print("Ошибка. Нет такой кнопки или пагинация закончилась")
        return False
    
    if next_button and next_button.is_displayed():
        next_button.click()
        return True
    else:
        return False
    
def click_size_guide(driver):
    try:
        modal_close_button = driver.find_element(By.CLASS_NAME, 'SkuPanel_sizeGuide__Phf6_')
        if modal_close_button:
            modal_close_button.click()
    except Exception as e:
        print("Нет всплывающего баннера")
        