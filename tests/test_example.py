import pytest
import requests


class TestExample:
    names = [
        ("Alex"),
        ("Artur"),
        ("")
    ]

    def test_check_math(self):
        a = 5
        b = 7
        result = 12
        assert a + b == result, f"Result isn't equals expected value: {result}"

    def test_check_math_two(self):
        a = 5
        b = 9
        result = 12
        assert a + b == result, f"Result isn't equals expected value: {result}"

    @pytest.mark.parametrize('name', names)
    def test_hello_url(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        payload = {'name': name}
        expected_text = ""

        response = requests.get(url, params=payload)
        assert response.status_code == 200, "Wrong response code"

        response_json = response.json()
        assert "answer" in response_json, "Response name isn't contains in response json!"

        if len(name) == 0:
            expected_text = "Hello, someone"
        else:
            expected_text = f"Hello, {name}"
        answer = response_json["answer"]
        assert answer == expected_text, "Expected text isn't equals response json"
