import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization epic")
class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_auth = self.get_json_value(response1, "user_id")

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test successfully authorize user by email and password")
    def test_user_auth(self):

        response2 = MyRequests.get(
            "user/auth",
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_auth,
            "Auth User is not equals Check User in the response"
        )

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test error authorize user without token and cookies")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):

        if condition == "no_cookie":
            response2 = MyRequests.get(
                "user/auth",
                headers={'x-csrf-token': self.token},
            )
        else:
            response2 = MyRequests.get(
                "user/auth",
                cookies={'auth_sid': self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorize with condition {condition}"
        )
