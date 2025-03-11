import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Edit user epic")
class TestUserEdit(BaseCase):

    def setup_method(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data["email"]
        self.first_name = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }
        response2 = MyRequests.post("user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test successful edit new user and successful get user data")
    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Changed Name"

        response = MyRequests.put(
            f"user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response, 200)

        # GET
        response2 = MyRequests.get(
            f"user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            new_name,
            "Wrong name after user edit!!!"
        )

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test edit new user without authorization")
    def test_edit_user_data_without_auth(self):
        # EDIT
        new_name = "Changed Name without auth"

        response = MyRequests.put(
            f"user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "Auth token not supplied", "Something wrong with edit user"

    @allure.severity("normal")
    @allure.description("This test edit new user with authorization as other user")
    def test_edit_user_with_auth_other_user(self):
        register_data = self.prepare_registration_data()
        response5 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response5, 200)

        email = register_data["email"]
        password = register_data["password"]

        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name with auth other user"

        response3 = MyRequests.put(
            f"user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        assert response3.json()["error"] == "This user can only edit their own data.", "Something wrong with edit user"

    @allure.severity("normal")
    @allure.description("This test edit new user with wrong email")
    def test_edit_user_with_wrong_email(self):
        # EDIT
        new_email = "new12345email.com"

        response = MyRequests.put(
            f"user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "Invalid email format", "Something wrong with edit user"

    @allure.severity("normal")
    @allure.description("This test edit new user with short user name")
    def test_edit_user_with_short_first_name(self):
        # EDIT
        new_first_name = "A"

        response = MyRequests.put(
            f"user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, "error")
        assert response.json()["error"] == "The value for field `firstName` is too short", \
            "Something wrong with edit user"





