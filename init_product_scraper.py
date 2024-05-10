import asyncio, selenium_async
from selenium_async import Pool
from functools import partial
from utils import get_splited_urls
from product_scraper import ProductScraper

def start_driver(driver: selenium_async.WebDriver, driver_urls):
    product_scraper = ProductScraper(urls_to_scrap=driver_urls, driver=driver)
    product_scraper.init_scrap_products()
    return driver


async def init_product_scraper_async(all_products=[], num_drivers = 1):
    driver_urls = get_splited_urls(num_drivers, all_products)
    tasks = []
    for urls in driver_urls:
        partial_func = partial(start_driver, driver_urls=urls)
        tasks.append(selenium_async.run_sync(partial_func, pool=Pool(max_size=num_drivers, blank_page_after_use=True)))

    drivers = await asyncio.gather(*tasks)
    for driver in drivers:
        driver.quit()



if __name__ == "__main__":
    asyncio.run(init_product_scraper_async([("https://www.poizon.com/product/nike-mercurial-superfly-7-pinkred-black-gray-52581488", "Basketball"),]))
