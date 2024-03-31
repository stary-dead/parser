import selenium_async
from selenium_async import WebDriver
import asyncio
import time
from functools import partial
import request_sender
print(1)
# def get_title1(driver: selenium_async.WebDriver, data):
#     driver.get(url = "https://www.python.org/")
#     time.sleep(10)
#     print(data)
#     return driver.title
# def get_title2(driver: selenium_async.WebDriver, data):
#     driver.get(url = "https://www.youtube.com/")
#     print(data)
#     return driver.title
# def get_title3(driver: selenium_async.WebDriver, data):
#     driver.get(url = "https://www.google.com/")
#     time.sleep(15)
#     print(data)
    
#     return driver.title
# async def main():
#      tasks = []
#     #  options = Options(browser="firefox", headless=None)
#     #  driver = await selenium_async.run_sync()
#      partial_get_title1 = partial(get_title1, data="Ну")
#      partial_get_title2 = partial(get_title2, data="Да")
#      partial_get_title3 = partial(get_title3, data="Нахуй")
#      tasks.append(selenium_async.run_sync(partial_get_title1))
#      tasks.append(selenium_async.run_sync(partial_get_title2))
#      tasks.append(selenium_async.run_sync(partial_get_title3))
#      await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())

# # prints: Welcome to Python.org