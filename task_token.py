import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
sleep_time = response.json()["seconds"]
task_token = response.json()["token"]

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": task_token})
if response.json()["status"] == "Job is NOT ready":
    print(f"Ожидаем выполнения задачи: {sleep_time} секунд")
    time.sleep(sleep_time)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": task_token})
if (response.json()["status"] == "Job is ready") and "result" in response.text:
    print(response.json()["status"])
    print(response.json()["result"])