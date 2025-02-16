import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(len(response.history))
print(response.history[-1].url)

