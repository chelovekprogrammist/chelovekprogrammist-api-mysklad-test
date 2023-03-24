import requests
import os

def find_product_id(barcode):
    mySklad_api_key = os.getenv('MY_SKLAD_API_KEY')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": mySklad_api_key
    }

    # Получаем список товаров
    url = f'https://online.moysklad.ru/api/remap/1.2/entity/product?filter=barcode={barcode}' # Поиск по штрихкоду происходит по фильтру а не поиском
    response = requests.get(url, headers=headers)

    products = response.json()['rows'] # Получаем информаци товара и переводим в json форма

    id_produkt = products[0]['meta']['href'] # Вытаскиваем it товара

    return id_produkt
