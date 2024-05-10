import aiohttp
import asyncio
import json
import os
import aiofiles

url = "https://new.yoocart.ru/action/parse-poison/import-json.php?code=h2mseventyn"
def get_folder_names(directory = "results"):
    folder_names = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folder_names.append(item)
    return folder_names

async def send_post_request(url, data):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:                    
                    if response.status == 200:
                        print(f"Response status: {response.status}")
                        print(await response.text())
                        break
                    else:
                        print(f"Response status: {response.status}\nRetrying in 5 minutes...")
                        await asyncio.sleep(60)
        except asyncio.TimeoutError as e:
            print(f"Timeout error\nRetrying in 5 minutes...")
            await asyncio.sleep(300)

async def read_file_async(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        return await file.read()

async def process_files(files):
    products_to_send = []
    for file_path in files:
        file_content = await read_file_async(file_path)
        product_data = json.loads(file_content)
        products_to_send.append(product_data)
        if len(products_to_send) == 120: # Cколько товаров отправляем
            await send_post_request(url, products_to_send)
            await asyncio.sleep(60*2) # С какой периодичностью, секунды
            products_to_send = []
    if products_to_send:
        await send_post_request(url, products_to_send)

async def main(category_name):
    result_folder = 'results/'+category_name

    files_to_process = []
    for filename in os.listdir(result_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(result_folder, filename)
            files_to_process.append(file_path)

    await process_files(files_to_process)
    
if __name__ == "__main__":
	categories = get_folder_names()
	for category in categories:
		asyncio.run(main(category))
