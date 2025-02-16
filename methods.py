import requests

# 1) Делает http-запрос любого типа без параметра method
# В этом случае выводится 'Wrong method provided' для POST, GET, PUT, DELETE
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)
print("\n")

# 2) Делает http-запрос не из списка
# Делаю запросы HEAD - 400 ответ, PATCH - 400 ответ 'Wrong HTTP method'
response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "PATCH"})
print(response.status_code)
print(response.text)
print("\n")

# 3) Делает запрос с правильным значением method
# Приходит код - 200, ответ - {"success":"!"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.status_code)
print(response.text)
print("\n")

# 4) С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method
params = ['{"method": "GET"}', '{"method": "POST"}', '{"method": "PUT"}', '{"method": "DELETE"}']
for param in params:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
    print("GET - " + response.text + " " + param)
    response_2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print("POST - " + response_2.text + " " + param)
    response_3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print("PUT - " + response_3.text + " " + param)
    response_4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print("DELETE - " + response_4.text + " " + param)
    print("\n")

# DELETE - тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок
# GET, POST - типы совпадают, но сервер считает, что это не так
