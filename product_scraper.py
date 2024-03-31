import asyncio
from scraper import parse_product_content
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product import Product
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import selenium_async
from selenium_async import Pool
from functools import partial

def get_splited_urls(driver_count, urls):
    num_drivers = [[] for _ in range(driver_count)]

    for index, url in enumerate(urls):
        num_driver_index = index % driver_count
        num_drivers[num_driver_index].append(url)
    return num_drivers

def start_driver(driver: selenium_async.WebDriver, driver_urls):
    for product in driver_urls:
        parse_product_content(driver, product)


async def start_parse_products(all_products=[]):
    num_drivers = 6 
    driver_urls = get_splited_urls(num_drivers, all_products)
    tasks = []
    for urls in driver_urls:
        partial_func = partial(start_driver, driver_urls=urls)
        tasks.append(selenium_async.run_sync(partial_func, pool=Pool(max_size=num_drivers, blank_page_after_use=True)))

    # Запускаем все задачи параллельно
    await asyncio.gather(*tasks)

# asyncio.run(start_parse_products())
