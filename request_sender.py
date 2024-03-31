import aiohttp
import asyncio
import json
import os
import aiofiles

url = "https://new.yoocart.ru/action/parse-poison/import-json.php?code=h2mseventyn"
async def send_post_request(url, data):
    print(data)
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, json=data) as response:
    #         print(f"Response status: {response.status}")
    #         print(await response.text())

async def read_file_async(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        return await file.read()

async def process_files(files):
    products_to_send = []
    for file_path in files:
        file_content = await read_file_async(file_path)
        product_data = json.loads(file_content)
        products_to_send.append(product_data)
        if len(products_to_send) == 50:
            await send_post_request(url, products_to_send)
            await asyncio.sleep(60*10) 
            products_to_send = []
    if products_to_send:
        await send_post_request(url, products_to_send)

async def main():
    result_folder = 'results'

    files_to_process = []
    for filename in os.listdir(result_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(result_folder, filename)
            files_to_process.append(file_path)

    await process_files(files_to_process)
        
