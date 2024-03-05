import asyncio
import time
from scraper import parse_category
from utils import calculate_execution_time
from product_scraper import start_parse_products
async def main(categories):
    start_time = time.time()  # сохраняем время начала выполнения скрипта
    semaphore = asyncio.Semaphore(2)  # Ограничение на две одновременно выполняемые задачи

    tasks = [parse_category(semaphore, category) for category in categories]
    results = await asyncio.gather(*tasks)

    # Объединяем списки продуктов из всех категорий в один список
    all_products = [product for products in results for product in products]
    await start_parse_products(all_products)

    
    total_time = calculate_execution_time(start_time)
    print(f"Общее время выполнения: {total_time} секунд")
    print(f"Количество обработанных категорий: {len(categories)}")
    print(f"Общее количество продуктов по всем категориям: {len(all_products)}")

    
if __name__ == "__main__":
    categories = [
        {'name': 'Категория 1', 'url': 'https://www.poizon.com/category/sneakers/basketball-500000368'},
        # {'name': 'Категория 2', 'url': 'https://www.poizon.com/category/sneakers/skateboarding-500000370'},
        # Добавьте дополнительные категории по аналогии
    ]
    products = [
        ("https://www.poizon.com/product/jordan-11-retro-dmp-gratitude-2023-64839289", "https://google.com"),
        ("https://www.poizon.com/product/converse-chuck-taylor-all-star-70-hi-black-52308433", "https://google.com"),
        ("https://www.poizon.com/product/nike-air-monarch-iv-white-navy-52565620", "https://google.com"),
        ("https://www.poizon.com/product/nike-air-force-1-low-07-white-52579883", "https://google.com"),
        ("https://www.poizon.com/product/nike-dunk-low-retro-white-black-panda-52581981", "https://google.com"),
        ("https://www.poizon.com/product/nike-air-force-1-low-flax-52577285", "https://google.com"),
    ]
    # asyncio.run(main(categories))
    asyncio.run(start_parse_products(products))
