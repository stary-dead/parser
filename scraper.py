# scraper.py
import asyncio
import re
from bs4 import BeautifulSoup
from utils import *
from product import Product
from datetime import datetime
import time
async def parse_page(driver, name_category):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    goods_list = soup.find('div', class_=re.compile(r'GoodsList_goodsList__\w+'))


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

async def parse_category(semaphore, category):
    async with semaphore:
        
        base_url = category['url']
        name_category = category['name']
        driver = initialize_webdriver(base_url)
        await asyncio.sleep(4)
        processed_pages = 0
        total_count_items = 0
        total_items = []
        while True:
            await asyncio.sleep(5)
            count_items_on_page, items_on_page = await parse_page(driver, name_category)
            print("__________________________________________")
            print(items_on_page)
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
    name_category = data[1] # data - кортеж вида (url, category_name)
    print(url)

    driver.get(url)
    time.sleep(5)
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
    pattern = r'(US|UK)\s*([MW]?)\s*(\d+(\.\d+)?)?\s*([YCY]?)?\s*'
    sku_panel = None
    found_size = False
    for panel in soup.findAll('div', class_=re.compile(r'SkuPanel_list__\w+')):
        sizes = panel.findAll('div', class_=re.compile(r'SkuPanel_value__\w+'))
        if(sizes):
            for item in sizes:
                size = item.text.strip()
                if re.fullmatch(pattern, size):
                    sku_panel = panel
                    found_size = True
                    break
                else:
                    continue
        if found_size:
            break

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

    image_wrapper = soup.find('div', class_=re.compile(r'ProductSkuImgs_selectImg__\w+'))
    if image_wrapper:
        images = image_wrapper.findAll('img', class_=re.compile(r'ProductSkuImgs_img__\w+'))
        links_to_image = []
        for image in images:
            links_to_image.append(image['src'])
    else:
        print("Блок с картинками не найден")

    product = Product(name, url, links_to_image, product_info, product_properties, name_category)
    product.save()
    print("____________________________________________________")
    return name, url, links_to_image, product_info, product_properties, name_category

