import pytest
import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Register user epic")
class TestUserRegister(BaseCase):
    data = [
        {
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com',
            'response': 'password'},
        {
            'password': '123',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com',
            'response': 'username'},
        {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com',
            'response': 'firstName'},
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'email': 'vinkotov@example.com',
            'response': 'lastName'},
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'response': 'email'}
    ]

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test successful register user")
    def test_create_user_successful(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test register user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.tag("smoke")
    @allure.severity("critical")
    @allure.description("This test register user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'email': email
        }

        response = MyRequests.post("user/", data=data)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.content.decode("utf-8") == "Invalid email format", f"Valid email format: '{response.content}'"

    @allure.description("This test register user without parameters")
    @pytest.mark.parametrize('parameters', data)
    def test_create_user_without_parameters(self, parameters):
        response = MyRequests.post("user/", data=parameters)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {parameters.get('response')}", f"Unexpected required params parameters '{response.content}'"

    @allure.severity("normal")
    @allure.description("This test register user with short name")
    def test_create_user_with_short_name(self):
        firstName = 'l'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    @allure.severity("normal")
    @allure.description("This test register user with long name more than 250 chars")
    def test_create_user_with_long_name(self):
        firstName = 'feoirgeoirgeprgjeprigjoerigoeirgoeirjgoeirgjoeigoeirgeoirgneorgneorgjperojgwpojrgowirjgiehgoeirgwpjwlfkwe;fmw;efw;egwogoepgojrgiojeoigjeorjgpwrogjeiorjgioehrgpwrjgwoirhgjoehrgoeijrgoiehrgpoejrpgoejprgjeporgjeprogjeporgjeporgjeporgjeporgeprojgpejgpoowefw'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'firstName' field is too long", f"Unexpected response content {response.content}"
