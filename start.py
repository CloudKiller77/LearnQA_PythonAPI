import requests

response = requests.get("https://playground.learnqa.ru/api/hello")
print(response.text)
print("Hello from Алексей")