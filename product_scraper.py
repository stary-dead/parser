import re, utils, time
from bs4 import BeautifulSoup
from product import Product
from selenium.common.exceptions import TimeoutException
class ProductScraper:
    def __init__(self, urls_to_scrap, driver):
        self.urls = urls_to_scrap
        self.driver = driver

    def init_scrap_products(self):
        for product in self.urls:
            self.parse_product_content(product)

    def open_page(self, url):        
        print(url)
        self.driver.get(url)
        time.sleep(4)

    def get_html_content(self):
        return self.driver.page_source
    
    def get_soup(self):
        html_content = self.get_html_content()
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    
    def scrap_title(self, soup):
        main_info = soup.find('h1', class_=re.compile(r'MainInfo_title__\w+'))
        if main_info:
            name = main_info.text.strip()
        else:
            print("Блок с названием не найден")
            name = "None"
        return name
    
    def scrap_sizes_info(self, soup):
        pattern = r'(US|UK)\s*(Kids)?\s*([MW]?)\s*(\d+(\.\d+)?)?\s*([YCY]?)?\s*'
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

        return product_info
    
    def scrap_product_properties(self, soup):
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

        return product_properties
    
    def scrap_product_images(self, soup):
        image_wrapper = soup.find('div', class_=re.compile(r'ProductSkuImgs_selectImg__\w+'))
        links_to_image = []
        if image_wrapper:
            images = image_wrapper.findAll('img', class_=re.compile(r'ProductSkuImgs_img__\w+'))
            for image in images:
                links_to_image.append(image['src'])
        else:
            print("Блок с картинками не найден")
        return links_to_image
    
    def scrap_product_size_guide(self):
        utils.click_size_guide(self.driver)
        time.sleep(2)
        soup = self.get_soup()
        columns = soup.findAll('div', class_=re.compile(r'size-guide_column__\w+'))
        table = []
        if columns:
            num_rows = len(columns[0].findAll('div', class_=re.compile(r'size-guide_tableCell__\w+')))
            num_columns = len(columns)
            headers = soup.findAll('div', class_=re.compile(r'size-guide_tableHeader__\w+'))
            
            # Создаем пустой двумерный массив
            table = [['' for _ in range(num_columns)] for _ in range(num_rows + 1)]

            # Заполняем первую строку заголовками
            for i, header in enumerate(headers):
                table[0][i] = header.text.strip()

            # Заполняем остальные строки данными из каждой ячейки
            for i, column in enumerate(columns):
                cells = column.findAll('div', class_=re.compile(r'size-guide_tableCell__\w+'))
                for j, cell in enumerate(cells):
                    table[j + 1][i] = cell.text.strip()  # Добавляем 1 к j, чтобы пропустить первую строку

        else:
            print('Не нашелся')

        return table
    
    def parse_product_content(self, data):
        url = data[0]
        name_category = data[1] # data - кортеж вида (url, category_name)
        try:
            self.open_page(url)  
        except TimeoutException as e:
            print(f"Парсинг страницы {url} не завершен. Страница не прогрузилась")     
        utils.close_modal(self.driver)
        soup = self.get_soup()
        name = self.scrap_title(soup)

        
        time.sleep(2)
        soup = self.get_soup()
        
        product_info = self.scrap_sizes_info(soup)
        product_properties = self.scrap_product_properties(soup)
        product_images = self.scrap_product_images(soup)

        product_size_guide = self.scrap_product_size_guide()

        product = Product(name, url, product_images, product_info, product_properties, name_category, product_size_guide)
        if not product.save():
            print(f"Продукт {product.name} не был записан из-за отсутсвия поля")
        print("____________________________________________________")
        return name, url, product_images, product_info, product_properties, name_category, product_size_guide
