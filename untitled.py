from datetime import datetime

shipment_date_1 = '2023-02-28T13:00:00Z'
shipment_date_2 = datetime.fromisoformat(shipment_date_1)
url = "https://online.moysklad.ru/api/remap/1.2/entity/customerorder"
print()