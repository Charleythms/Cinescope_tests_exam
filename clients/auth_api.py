from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL


class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def login_user(self, login_data, expected_status=200):
        return self.send_request("POST", "/login", data=login_data, expected_status=expected_status)

    def authenticate(self, user_creds):
        response = self.login_user({
            "email": user_creds[0],
            "password": user_creds[1]
        }).json()
        self._update_session_headers({"authorization": "Bearer " + response["accessToken"]})