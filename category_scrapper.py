import re
from bs4 import BeautifulSoup
import asyncio
import utils

class CategoryScrapper:

    def __init__(self, category) -> None:
        base_url = category['url']
        self.driver = utils.initialize_webdriver(base_url)
        self.category = category
    
    async def scrap_products_on_page_async(self):
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        goods_list = soup.find('div', class_=re.compile(r'GoodsList_goodsList__\w+'))
        name_category = self.category['name']

        if goods_list:
            list_articles = goods_list.find_all('a', class_=re.compile(r'GoodsItem_goodsItem__\w+'))
            
            products = []
            for article in list_articles:
                product_url = article['href']
                
                product = ("https://www.poizon.com"+product_url, name_category)
                products.append(product)
            
            return len(list_articles), products
        else:
            print("Блок с товарами не найден")
            return 0, []
        
    async def explore_category_pages_async(self):
        try:
            await asyncio.sleep(4)
            processed_pages = 0
            total_count_items = 0
            total_items = []
            while True:
                await asyncio.sleep(5)
                count_items_on_page, items_on_page = await self.scrap_products_on_page_async()
                print("__________________________________________")
                print(count_items_on_page)
                print("__________________________________________")
                total_count_items += count_items_on_page
                total_items.extend(items_on_page)
                processed_pages += 1
                
                try:
                    utils.close_modal(self.driver)
                    await asyncio.sleep(2)
                    if utils.click_next_page(self.driver):
                        continue
                    else:
                        print("Больше страниц нет. Инициализация парсинга отдельных товаров")
                        break
                except Exception as e:
                    print("Ошибка CategoryScraper.explore_category_pages_async: ", e)
                    break
        except Exception as e:
            print("Ошибка CategoryScrapper, message: ")
        finally:
            self.driver.quit()

        return total_items
