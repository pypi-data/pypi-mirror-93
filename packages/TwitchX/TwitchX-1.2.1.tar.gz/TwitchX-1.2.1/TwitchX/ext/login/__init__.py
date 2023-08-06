import requests
import browser_cookie3
from requests.utils import dict_from_cookiejar
from TwitchX.error import TwoFactorAuthenticationEnabled
from TwitchX.error import LoginVerificationCodeRequired
from TwitchX.error import InvalidPassword
from TwitchX.error import CAPTCHARequired

from TwitchX.util import HTTPUtil


class TwitchAccount(HTTPUtil):
    def __init__(self, client_id: str, username: str, password: str):
        """Twitch Login

        :param client_id:
        :type client_id:
        :param username:
        :type username:
        :param password:
        :type password:
        """

        self.login_form_url = "https://www.twitch.tv/login"
        self.login_post_url = "https://passport.twitch.tv/login"
        self.user_agent = self.get_user_agent()["User-Agent"]
        self.cookies = []

        self.client_id = client_id
        self.client_token = None
        self.username = username
        self.password = password

        self.session = requests.session()
        self.session.headers.update(
            {
                "Client-ID": self.client_id, "User-Agent": self.user_agent
            }
        )
        super(TwitchAccount, self).__init__()

        self.ext = self

    @staticmethod
    async def _login_helper():
        twitch_domain = ".twitch.tv"
        cookie_jar = browser_cookie3.firefox(domain_name=twitch_domain)
        cookies_dict: dict = dict_from_cookiejar(cookie_jar)
        return cookies_dict

    @staticmethod
    async def _captcha_proof(response, payload):
        if "captcha_proof" in response:
            payload["captcha"] = dict(proof=response["captcha_proof"])
        return payload

    @staticmethod
    async def _error_handler(response):
        if "error_code" in response:
            err_code = response["error_code"]
            if err_code == 3011 or err_code == 3012:
                raise TwoFactorAuthenticationEnabled("Two factor authentication enabled.")
            elif err_code == 3022 or err_code == 3023:
                return True
            elif err_code == 3001:
                raise InvalidPassword("Invalid username or password")
            elif err_code == 1000:
                return True
            else:
                raise NotImplementedError(
                    f"Unknown TwitchAPI error code: {err_code}"
                )

    async def _backup_flow(self, _use_backup_flow: bool, _captcha_proof: dict):
        """backup login task

        :param _use_backup_flow: status
        :type _use_backup_flow: bool
        :param _captcha_proof: captcha proof
        :type _captcha_proof: dict
        :return:
        :rtype:
        """
        if _use_backup_flow:
            helper = await self._login_helper()
            return helper
        else:
            try_login = await self._login_request(json_data=_captcha_proof)
            return try_login

    async def _login_request(self, json_data):
        r = self.session.post(self.login_post_url, json=json_data)
        t = r.json()
        return t

    async def get_cookie(self):
        payload = dict(
            client_id=self.client_id,
            username=self.username,
            password=self.password,
            undelete_user=False,
            remember_me=True
        )
        res = await self._login_request(json_data=payload)
        _captcha_proof, _use_backup_flow = (
            await self._captcha_proof(response=res, payload=payload),
            await self._error_handler(response=res)
        )
        return await self._backup_flow(_use_backup_flow, _captcha_proof)
