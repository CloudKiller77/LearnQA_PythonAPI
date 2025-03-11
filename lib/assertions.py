from requests import Response
import json
import allure


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        with allure.step(f"Assert response json value by expected name: '{name}'"):
            assert name in response_dict, f"Response JSON doesn't have key '{name}'"
            assert response_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        with allure.step(f"Assert response json has expected name: '{name}'"):
            assert name in response_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        for name in names:
            with allure.step(f"Assert response json has expected name from dictionary names: '{name}'"):
                assert name in response_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_status_code(response: Response, expected_code):
        with allure.step(f"Assert response has expected status code: '{expected_code}'"):
            assert response.status_code == expected_code, \
                f"Unexpected status code: {expected_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"
        with allure.step(f"Assert response json hasn't expected name: '{name}'"):
            assert name not in response_dict, f"Response JSON shouldn't have key '{name}'. But it's present"
