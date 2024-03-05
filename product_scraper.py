import asyncio
from scraper import parse_product_content
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product import Product
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


async def start_parse_products(all_products=[]):
    num_links = len(all_products)
    num_tabs_per_driver = 4  # Количество вкладок на один драйвер
    num_drivers = 3 

    sem = asyncio.Semaphore(num_drivers)
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    handles = []
    for _ in range(num_tabs_per_driver):
        driver.execute_script("window.open('about:blank');")
        handles.append(driver.window_handles[-1])

    tasks = []
    for i, product in enumerate(all_products):
        task = asyncio.create_task(parse_product_content(sem, driver, handles[i % num_tabs_per_driver], product))
        tasks.append(task)


    results = await asyncio.gather(*tasks)
    # driver.quit()


# async def start_parse_products(all_products = []):
#     sem = asyncio.Semaphore(8)  # Ограничение на две одновременные задачи
#     tasks = [parse_product_content(sem, data) for data in all_products]
#     results = await asyncio.gather(*tasks)

    # for idx, result in enumerate(results):
    #     if result is None:
    #         # print(f"Проблема с URL: {product_urls[idx]}")
    #         continue
    #     product_name, product_url, product_image_url, product_info, product_properties = result

    #     product = Product(product_url,product_image_url, product_info, product_properties)
    #     product.save()
        # filename = f"results/product_{idx + 1}.txt"
        # with open(filename, 'w', encoding='utf-8') as file:
        #     if product_info:
        #         file.write("Информация о размерах и ценах:\n")
        #         for item in product_info:
        #             file.write(f"Размер: {item['size']}, Цена: {item['price']}\n")
        #     else:
        #         file.write("Не удалось получить информацию о размерах и ценах товара\n")
        #     if product_properties:
        #         file.write("Информация о параметрах:\n")
        #         for item in product_properties:
        #             file.write(f"{item['label']} : {item['value']}\n")

# asyncio.run(start_parse_products())
