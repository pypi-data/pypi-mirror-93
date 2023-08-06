from TwitchX.util import HTTPUtil
from TwitchX.ext.login.browser import Browser


class TwitchAccount(HTTPUtil):
    def __init__(
            self,
            client_id: str,
            username: str,
            password: str,
            gmail_id: str,
            gmail_pw: str,
            headless: bool,
            driver_path: str
    ):
        """Twitch Login

        :param client_id:
        :param username:
        :param password:
        :param gmail_id:
        :param gmail_pw:
        :param headless:
        :param driver_path:
        """
        self.user_agent = self.get_user_agent()["User-Agent"]
        self.client_id = client_id

        self.username = username
        self.password = password
        self.gmail_id = gmail_id
        self.gmail_pw = gmail_pw
        self.headless = headless
        self.driver_path = driver_path
        super(TwitchAccount, self).__init__()

        self.ext = self

    async def get_cookies(self) -> dict:
        task = Browser(
            user_id=self.username,
            password=self.password,
            gmail_id=self.gmail_id,
            gmail_pw=self.gmail_pw,
            user_agent=self.user_agent,
            headless=self.headless,
            driver_path=self.driver_path
        )
        cookies = await task.get_login_cookie()
        return cookies
