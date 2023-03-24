import json
import requests
import os

client_id = os.getenv("SELLER_ID")
api_key = os.getenv("OZON_API_KEY")

def handle_response(data):
    # Получаем тип сообщения
    message_type = data.get("message_type")
    print("Тип сообщения:", message_type)
    
    # Получаем Номенр отправления
    posting_number = data.get("posting_number")
    print("Номенр отправления:", posting_number)
    
    # Получаем Информация о товарах
    products = data.get("products")
    print("Информация о товарах:", products)
    
    # Получаем SKU товара
    sku = data["products"][0]["sku"]
    print("SKU товара", sku)
    
    # Получаем Количество товара
    quantity = data["products"][0]["quantity"]
    print("Количество товара", quantity)
    
    # Получаем Дата и время начала обработки отправления в формате UTC.
    in_process_at = data.get("in_process_at")
    print("Дата и время начала обработки отправления в формате UTC .", in_process_at)
    
    #И дентификатор склада, на котором хранятся товары для этого отправления
    warehouse_id = data.get("warehouse_id")
    print("Склад ID:", warehouse_id)
    
    # Здесь можно выполнить необходимую обработку данных
    response_data = {"result": True}
    return response_data



#  Получаем информацию о товаре по sku  и выводим штрих код
def get_product_info(sku_value):
    url = 'https://api-seller.ozon.ru/v2/product/info'  # указываем url для запроса
    accepted_sku_value = sku_value

    # Параметры запроса
    
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    params = {
        "sku": accepted_sku_value #Здесь указываем полученую переменную sku товара
    }

    # Выполнение запроса 
    response = requests.post(url, headers=headers, json=params) 
    print ("ОТВЕТ response", response)
    return  response


# Получаем информациюинформацию о отправлению 
def get_shipping_info_by_id(posting_number_get_shipping_info_by_id):
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'  # указываем url для запроса отправлени
    
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    params ={
        "posting_number": posting_number_get_shipping_info_by_id,
        "with": {
        "analytics_data": False,
        "barcodes": False,
        "financial_data": False,
        "product_exemplars": False,
        "translit": False
        }
    }

    # Выполнение запроса 
    response_get_shipping_info_by_id = requests.post(url, headers=headers, json=params)

    print ("ОТВЕТ получения ответа по отправлению", response_get_shipping_info_by_id)
    return  response_get_shipping_info_by_id


