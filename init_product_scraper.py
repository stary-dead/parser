import asyncio, selenium_async
from selenium_async import Pool
from functools import partial
from utils import get_splited_urls
from product_scraper import ProductScraper

def start_driver(driver: selenium_async.WebDriver, driver_urls):
    product_scraper = ProductScraper(urls_to_scrap=driver_urls, driver=driver)
    product_scraper.init_scrap_products()

async def init_product_scraper_async(all_products=[], num_drivers = 1):
    driver_urls = get_splited_urls(num_drivers, all_products)
    tasks = []
    for urls in driver_urls:
        partial_func = partial(start_driver, driver_urls=urls)
        tasks.append(selenium_async.run_sync(partial_func, pool=Pool(max_size=num_drivers, blank_page_after_use=True)))

    await asyncio.gather(*tasks)

# asyncio.run(init_product_scraper_async([("https://www.poizon.com/product/jordan-courtside-23-white-dark-concord-gs-52421111", "Тестовая")]))
