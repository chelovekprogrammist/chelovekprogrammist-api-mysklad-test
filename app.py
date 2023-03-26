from flask import Flask, request
from response_handler import handle_response, get_product_info,get_shipping_info_by_id
from resend_mySklad import send_to_mySklad
from identifikator_pozici_po_barcode import find_product_id
import json
from datetime import datetime

app = Flask(__name__)

# задаем декоратор маршрутизации и обрабатываем POST запросы на этот маршрут

@app.route('/', methods=['POST'])
def receive_ping():
    data = request.json
    print("Received data: ", json.dumps(data, indent=4))

    if "message_type" in data and data["message_type"] == "TYPE_PING":
        response_data = {
            "version": "1.0",
            "name": "MyApp",
            "time": datetime.now()
        }
        return json.dumps(response_data), 200

    elif "message_type" in data:
        # обрабатываем любое другое сообщение
        response_data = {"result": True}

        # Получаем данные заказа
        sku_value = data['products'][0]['sku']                         # Получаем sku
        quantity = data['products'][0]['quantity']                     # Получаем количество товара
        # Запроса к Озону по Api для получении информации о полной информации о товаре
        info_pozishion = get_product_info(sku_value)                   # В этой переменной записывается ответ функции 
        all_info_position = info_pozishion.json()                      # Дешифровывает ответ в формат json
        barCod = all_info_position['result']['barcodes'][0]            # Вытаскиваем штрих код из информации о товаре озон

        posting_number = data['posting_number']                        # Получаем номер отправления
        shipping_info = get_shipping_info_by_id(posting_number)        # Получаю информацию об отправвления
        shipping_info_json = shipping_info.json()                      # Дешифровывает ответ в формат json
        price = shipping_info_json['result']['products'][0]['price']   # Вытаскиваем Получаем цену из отправления 

        # Склад отгрузки
        # Получаем номер склада куда нужно отнести отправление
        warehouse_id_number = shipping_info_json['result']['delivery_method']['warehouse']

        # Планируемая дата отгрузки
        # Получаем планируемую дату отгрузки
        shipment_date = shipping_info_json['result']['shipment_date']
        
        print("*******************", shipping_info.json())
        print("Доставка на склад", shipment_date)
        
        id_produkt = find_product_id(barCod)  # получения идентификатора товара от мой склад

      
        # Передаем данные пуш ответа на обработку другой функции   
        result = handle_response(data)            #  message_type(Необязательно)
        send_to_mySklad(id_produkt, quantity, price, posting_number, warehouse_id_number, shipment_date)     #  И Передаю id позиции, количество, цена продажи в файл формирования запроса на создание товара
        
        return json.dumps(response_data), 200
         
    elif "message_type" in data:

        return json.dumps(response_data), 200


    else:
        # формируем ответ об ошибке в соответствии с требованиями API OZON
        response_data = {
            "error": {
                "code": "ERROR_PARAMETER_VALUE_MISSED",
                "message": "Parameter 'message_type' is missing or has an invalid value",
                "details": None
            }
        }
        return json.dumps(response_data), 400
    
if __name__ == '__main__':
    app.run(port=7378, debug=True)
