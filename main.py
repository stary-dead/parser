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
    {'name': 'Basketball', 'url': 'https://www.poizon.com/category/sneakers/basketball-500000368'},
    # {'name': 'Skateboarding', 'url': 'https://www.poizon.com/category/sneakers/skateboarding-500000370'},
    # {'name': 'Lifestyle', 'url': 'https://www.poizon.com/category/sneakers/lifestyle-500000372'},
    # {'name': 'Running', 'url': 'https://www.poizon.com/category/sneakers/running-500000374'},
    # {'name': 'Training', 'url': 'https://www.poizon.com/category/sneakers/training-500000376'},
    # {'name': 'Cleats', 'url': 'https://www.poizon.com/category/sneakers/cleats-500000378'},
    # {'name': 'Outdoors', 'url': 'https://www.poizon.com/category/sneakers/outdoors-500000380'},
    # {'name': 'Boots', 'url': 'https://www.poizon.com/category/shoes/boots-500000382'},
    # {'name': 'Flats', 'url': 'https://www.poizon.com/category/shoes/flats-500000389'},
    # {'name': 'Casual Shoes', 'url': 'https://www.poizon.com/category/shoes/casual-shoes-500000391'},
    # {'name': 'Pumps', 'url': 'https://www.poizon.com/category/shoes/pumps-500000393'},
    # {'name': 'Sandals & Flip Flops', 'url': 'https://www.poizon.com/category/shoes/sandals-flip-flops-500000395'},
    # {'name': 'Dress Shoes', 'url': 'https://www.poizon.com/category/shoes/dress-shoes-500000398'},
]

    asyncio.run(main(categories))
    # asyncio.run(start_parse_products(products))
