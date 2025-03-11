import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Delete user epic")
class TestUserDelete(BaseCase):

    def setup_method(self):
        # REGISTER
        data = self.prepare_registration_data()

        response = MyRequests.post("user/", data=data)
        Assertions.assert_status_code(response, 200)

        email = data["email"]
        password = data["password"]
        self.user_id = self.get_json_value(response, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("user/login", data=login_data)
        Assertions.assert_status_code(response2, 200)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test delete user with wrong ID")
    def test_user_error_delete(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_auth = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(
            f"user/{user_id_auth}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_json_has_key(response2, "error")
        assert response2.json()["error"] == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            "Something wrong with delete user"

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test successful delete user")
    def test_user_success_delete(self):
        # DELETE
        response3 = MyRequests.delete(
            f"user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_status_code(response3, 200)
        assert response3.content.decode("utf-8") == '{"success":"!"}', f"User: {self.user_id} not deleted!"

        # GET
        response4 = MyRequests.get(f"user/{self.user_id}")

        Assertions.assert_status_code(response3, 200)
        assert response4.content.decode("utf-8") == "User not found", f"Something wrong with get user"

    @allure.severity("normal")
    @allure.description("This test delete user with authorization as other user")
    def test_user_error_delete_with_auth_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response1, 200)

        user_id = self.get_json_value(response1, "id")

        # DELETE
        response3 = MyRequests.delete(
            f"user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        assert response3.json()[
                   "error"] == "This user can only delete their own account.", "Something wrong with delete user"

