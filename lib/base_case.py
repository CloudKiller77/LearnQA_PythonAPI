import json.decoder
from datetime import datetime

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name) -> str:
        assert cookie_name in response.cookies, f"Cannot find cookie name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name) -> str:
        assert header_name in response.headers, f"Cannot find header name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name) -> str:
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        assert name in response_dict, f"Response JSON doesn't have key '{name}'"

        return response_dict[name]

    def prepare_registration_data(self, email=None) -> dict:
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'email': email
        }
