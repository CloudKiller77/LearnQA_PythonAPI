import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):

    def setup_method(self):
        # REGISTER
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)

        email = data["email"]
        password = data["password"]
        self.user_id = self.get_json_value(response, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    def test_user_error_delete(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_auth = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id_auth}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_json_has_key(response2, "error")
        assert response2.json()["error"] == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            "Something wrong with delete user"

    def test_user_success_delete(self):
        # DELETE
        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        print(response3.content)

        Assertions.assert_status_code(response3, 200)
        assert response3.content.decode("utf-8") == '{"success":"!"}', f"User: {self.user_id} not deleted!"

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}")
        print(response4.content)

        Assertions.assert_status_code(response3, 200)
        assert response4.content.decode("utf-8") == "User not found", f"Something wrong with get user"

    def test_user_error_delete_with_auth_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)

        user_id = self.get_json_value(response1, "id")

        # DELETE
        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        print(response3.content)

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        assert response3.json()[
                   "error"] == "This user can only delete their own account.", "Something wrong with delete user"

