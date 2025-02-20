import requests


class TestCheckCookie:

    def test_check_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

        response_cookie = response.cookies.get("HomeWork")
        # print(response_cookie)
        expected_cookie = "hw_value"

        assert response_cookie == expected_cookie, "Response cookie isn't equals expected cookie"
