import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):

    def setup_method(self):
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data["email"]
        self.first_name = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")
        print(self.user_id)

        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Changed Name"

        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response, 200)

        # GET
        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            new_name,
            "Wrong name after user edit!!!"
        )

    def test_edit_user_data_without_auth(self):
        # EDIT
        new_name = "Changed Name without auth"

        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "Auth token not supplied", "Something wrong with edit user"

    def test_edit_user_with_auth_other_user(self):
        register_data = self.prepare_registration_data()
        response5 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response5, 200)

        email = register_data["email"]
        password = register_data["password"]

        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name with auth other user"

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        assert response3.json()["error"] == "This user can only edit their own data.", "Something wrong with edit user"

    def test_edit_user_with_wrong_email(self):
        # EDIT
        new_email = "new12345email.com"

        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "Invalid email format", "Something wrong with edit user"

    def test_edit_user_with_short_first_name(self):
        # EDIT
        new_first_name = "A"

        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "The value for field `firstName` is too short", "Something wrong with edit user"





