import asyncio
import time
from scraper import parse_category
from utils import calculate_execution_time
from product_scraper import start_parse_products
import request_sender
async def main(categories):
    start_time = time.time()  # сохраняем время начала выполнения скрипта
    semaphore = asyncio.Semaphore(2)  # Ограничение на две одновременно выполняемые задачи

    tasks = [parse_category(semaphore, category) for category in categories]
    results = await asyncio.gather(*tasks)

    # Объединяем списки продуктов из всех категорий в один список
    all_products = [product for products in results for product in products]
    await start_parse_products(all_products)
    await request_sender.main()
    
    total_time = calculate_execution_time(start_time)
    print(f"Общее время выполнения: {total_time} секунд")
    print(f"Количество обработанных категорий: {len(categories)}")
    print(f"Общее количество продуктов по всем категориям: {len(all_products)}")

    
if __name__ == "__main__":
    categories = [
        # {'name': 'Категория 1', 'url': 'https://www.poizon.com/category/sneakers/basketball-500000368'},
        {'name': 'Категория 2', 'url': 'https://www.poizon.com/category/sneakers/skateboarding-500000370'},
        # Добавьте дополнительные категории по аналогии
    ]
    asyncio.run(main(categories))
    # asyncio.run(start_parse_products(products))
