import requests


class TestCheckHeader:

    def test_check_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")

        response_header = response.headers.get("x-secret-homework-header")
        # print(response_header)
        expected_header = "Some secret value"

        assert response_header == expected_header, "Response header isn't equals expected header"
