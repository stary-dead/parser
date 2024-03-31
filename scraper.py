# scraper.py
import asyncio
import re
from bs4 import BeautifulSoup
from utils import *
from product import Product
from datetime import datetime

async def parse_page(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    goods_list = soup.find('div', class_=re.compile(r'GoodsList_goodsList__\w+'))


    if goods_list:
        list_articles = goods_list.find_all('a', class_=re.compile(r'GoodsItem_goodsItem__\w+'))
        
        products = []
        for article in list_articles:
            # Получаем ссылку на изображение
            image_tag = article.find('img', class_=re.compile(r'PoizonImage_img__\w+'))
            if image_tag:
                image_url = image_tag['src']
            else:
                image_url = None

            # Получаем ссылку на товар
            product_url = article['href']  # Предполагается, что ссылка на товар находится в атрибуте href тега <a>
            
            product = ("https://www.poizon.com"+product_url, image_url)
            products.append(product)
        
        return len(list_articles), products
    else:
        print("Блок с товарами не найден")
        return 0, []

async def parse_category(semaphore, category):
    async with semaphore:
        
        base_url = category['url']
        driver = initialize_webdriver(base_url)
        await asyncio.sleep(4)
        processed_pages = 0
        total_count_items = 0
        total_items = []
        while True:
            await asyncio.sleep(5)
            count_items_on_page, items_on_page = await parse_page(driver)
            print("__________________________________________")
            print(count_items_on_page)
            print("__________________________________________")
            total_count_items += count_items_on_page
            total_items.extend(items_on_page)
            processed_pages += 1
            
            try:
                close_modal(driver)
                await asyncio.sleep(2)
                if click_next_page(driver):
                    continue
                else:
                    print("Программа была прервана.")
                    break
            except Exception as e:
                print("Ошибка parse_category:", e)
                break

        driver.quit()

        return total_items #returns list of turples [(url, link-to-image), (url, link-to-image),(url, link-to-image),]
    
#/___________________________________________________________\
# Далее код парсера отдельных товаров
#/___________________________________________________________\ 

def parse_product_content(driver, data):
    url = data[0]        
    link_to_image = data[1] # data - кортеж вида (url, link-to-image)
    print(url)

    driver.get(url)
    # await driver.get(url)
    html_content = driver.page_source  
    close_modal(driver)

    soup = BeautifulSoup(html_content, 'html.parser')
    main_info = soup.find('div', class_=re.compile(r'MainInfo_title__\w+'))
    if main_info:
        name = main_info.text.strip()
    else:
        print("Блок с названием не найден")
        name = "None"
    
    sku_panel = soup.find('div', class_=re.compile(r'SkuPanel_list__\w+'))
    if sku_panel:
        sku_items = sku_panel.find_all('div', class_=re.compile(r'SkuPanel_item__\w+'))
        product_info = []
        for sku_item in sku_items:
            size = sku_item.find('div', class_=re.compile(r'SkuPanel_value__\w+')).text.strip() if sku_item.find('div', class_=re.compile(r'SkuPanel_value__\w+')) else "None"
            price = sku_item.find('div', class_=re.compile(r'SkuPanel_price__\w+')).text.strip() if sku_item.find('div', class_=re.compile(r'SkuPanel_price__\w+')) else "None"

            product_info.append({'size': size, 'price': price})
    else:
        print("Блок с информацией о размерах и ценах товара не найден")
        product_info = None

    property_wrapper = soup.find('ul', class_=re.compile(r'ProductDetails_propertyWrapper__\w+'))
    if property_wrapper:
        property_items = property_wrapper.find_all('li', class_=re.compile(r'ProductDetails_propertyItem__\w+'))
        product_properties = []
        for item in property_items:
            label = item.find('span', class_=re.compile(r'ProductDetails_propertyLabel__\w+')).text.strip() if item.find('span', class_=re.compile(r'ProductDetails_propertyLabel__\w+')) else "None"
            value = item.find('span', class_=re.compile(r'ProductDetails_propertyValue__\w+')).text.strip() if item.find('span', class_=re.compile(r'ProductDetails_propertyValue__\w+')) else "None"

            product_properties.append({'label': label, 'value': value})
    else:
        print("Блок с дополнительными свойствами товара не найден")
        product_properties = None

    product = Product(name, url, link_to_image, product_info, product_properties)
    product.save()
    return name, url, link_to_image, product_info, product_properties

