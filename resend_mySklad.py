import requests
import json
from datetime import datetime, timedelta
import os


def send_to_mySklad(id_produkt, quantity, price, posting_number, warehouse_id_number, shipment_date):
    mySklad_api_key = os.environ.get('MY_SKLAD_API_KEY')
    url = "https://online.moysklad.ru/api/remap/1.2/entity/customerorder"

    # Изменяем формат даты и времени
    # Преобразование в объект datetime
    dt = datetime.fromisoformat(shipment_date.replace('Z','+00:00'))
    # Создаем объект timedelta с количеством часов, на которое нужно задвинуть время
    hours_to_add = 3
    delta = timedelta(hours=hours_to_add)

    # Добавляем timedelta к объекту datetime, чтобы задвинуть время на указанное количество часов
    dt_new = dt + delta



    # Преобразование в нужный формат
    shipment_date = dt_new.strftime('%Y-%m-%d %H:%M:%S')

    print(shipment_date) # "2023-02-28 13:00:00"


    headers = {
        "Content-Type": "application/json",
        "Authorization": mySklad_api_key
    }

    data = {
    "description": posting_number,              # Комментарий к заказу
    "shipmentAddress": warehouse_id_number,     # Добовляем адрес доставки
    "deliveryPlannedMoment": shipment_date,     # Добовляем плановую дату отгрузки

    # Информация о продавце
    "organization": {  
        "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/organization/b9d337b7-8be6-11eb-0a80-03d8000f4ff0",
            "type": "organization",
            "mediaType": "application/json"
        }
    },
    # Информация о контрагенте
    "agent": {        
        "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/3d4620db-8038-11ed-0a80-087e0007ab9a",
            "type": "counterparty",
            "mediaType": "application/json"
        }
    },
    # Информация о товаре
    "positions": [   
        {
            "quantity": float(quantity),
            "price": float(price) * 100, 
            "discount": 0,
            "vat": 0,
            "assortment": {
                "meta": {
                    "href": f"{id_produkt}",
                    "type": "product",
                    "mediaType": "application/json"
                }
            },
            "reserve": float(quantity)
        }
    ],
    # Добовляем Договор
    "contract": {
        "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/contract/5bc2ac85-8545-11ed-0a80-0140005fbc7c",
            "type": "contract",
            "mediaType": "application/json"
        }
    },
    # Добавляем проект
    "project": {
        "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/project/5c4b0753-7f80-11ed-0a80-00ec00364f0e",
            "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/project/metadata",
            "type": "project",
            "mediaType": "application/json"
        }
    },
    # Добовляем Канал продаж
    "salesChannel": {
        "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/saleschannel/6d7e3c31-252c-11ed-0a80-0e91000b94fe",
            "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/saleschannel/metadata",
            "type": "saleschannel",
            "mediaType": "application/json"
        }
    },
    # Добовляем Склад
    "store": {
        "meta":{
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/store/b9d44c3d-8be6-11eb-0a80-03d8000f4ff2",
            "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/store/metadata",
            "type": "store",
            "mediaType": "application/json",
        }
    }

}
          
    json_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=json_data)
    print(response.status_code)
    print(response.json())



