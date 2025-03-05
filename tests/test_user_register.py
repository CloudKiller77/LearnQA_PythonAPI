import datetime

import requests
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions


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

    def test_create_user_successful(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # print(response.content)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'leanrqa',
            'lastName': 'leanrqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # print(response.content)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.content.decode("utf-8") == "Invalid email format", f"Valid email format: '{response.content}'"

    @pytest.mark.parametrize('parameters', data)
    def test_create_user_without_parameters(self, parameters):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=parameters)
        # print(response.status_code)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {parameters.get('response')}", f"Unexpected required params parameters '{response.content}'"

    def test_create_user_with_short_name(self):
        firstName = 'l'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        firstName = 'feoirgeoirgeprgjeprigjoerigoeirgoeirjgoeirgjoeigoeirgeoirgneorgneorgjperojgwpojrgowirjgiehgoeirgwpjwlfkwe;fmw;efw;egwogoepgojrgiojeoigjeorjgpwrogjeiorjgioehrgpwrjgwoirhgjoehrgoeijrgoiehrgpoejrpgoejprgjeporgjeprogjeporgjeporgjeporgjeporgeprojgpejgpoowefw'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': firstName,
            'lastName': 'leanrqa',
            'email': 'vinkotov@example.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'firstName' field is too long", f"Unexpected response content {response.content}"
