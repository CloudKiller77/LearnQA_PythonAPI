import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Get user data epic")
class TestUserGet(BaseCase):

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
    @allure.description("This test try to get user data without authorization")
    def test_user_get_no_auth(self):
        response = MyRequests.get("user/2")

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')
        Assertions.assert_json_has_no_key(response, 'email')

    @allure.severity("normal")
    @allure.description("This test get user data successful")
    def test_get_user_details_auth_as_same_user(self):
        response2 = MyRequests.get(
            f"user/{self.user_id_auth}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.severity("normal")
    @allure.description("This test try to get user data authorized as other user")
    def test_get_user_details_auth_as_other_user(self):
        response2 = MyRequests.get(
            f"user/3",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_no_key(response2, 'firstName')
        Assertions.assert_json_has_no_key(response2, 'lastName')
        Assertions.assert_json_has_no_key(response2, 'email')
