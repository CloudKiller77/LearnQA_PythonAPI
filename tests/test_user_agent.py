import pytest
import requests


class TestUserAgent:
    exclude_params = [
        {
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'Android'},
        {
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'Chrome',
            'device': 'iOS'},
        {
            'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'platform': 'Googlebot',
            'browser': 'Unknown',
            'device': 'Unknown'},
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'platform': 'Web',
            'browser': 'Chrome',
            'device': 'No'},
        {
            'user-agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'iPhone'}
    ]

    @pytest.mark.parametrize('agents', exclude_params)
    def test_user_agent(self, agents):
        payload = {
            'User-Agent': agents.get("user-agent")
        }
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers=payload
        )
        # print(response.headers)
        # print(response.text)

        assert "platform" in response.json(), f"Response doesn't have 'platform'"

        expected_platform = agents.get("platform")
        expected_browser = agents.get("browser")
        expected_device = agents.get("device")

        assert response.json()["platform"] == expected_platform, f"Expected platform doesn't equals platform '{response.json()['platform']}'"
        assert response.json()["browser"] == expected_browser, f"Expected browser doesn't equals browser '{response.json()['browser']}'"
        assert response.json()["device"] == expected_device, f"Expected device doesn't equals device '{response.json()['device']}'"


# 2 'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'
#    в ответе получаем 'browser': 'No'

# 3 'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
#    в ответе получаем 'platform': 'Unknown'

# 5 'user-agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
#    в ответе получаем 'device': 'Unknown'
