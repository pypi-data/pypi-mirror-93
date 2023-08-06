from collections import ChainMap
from TwitchX.ext.login.browser._chrome import ChromeLogin
from TwitchX.ext.login.gmail import GmailParser


class Browser(GmailParser):
    def __init__(
            self,
            user_id: str,
            password: str,
            gmail_id: str,
            gmail_pw: str,
            user_agent: str,
            headless: bool,
            driver_path: str
    ):
        self._login_url = "https://www.twitch.tv/login"

        self.user_id = user_id
        self.password = password

        self.gmail_id = gmail_id
        self.gmail_pw = gmail_pw

        self.headless = headless
        self.user_agent = user_agent
        self.driver_path = driver_path
        self.chrome = ChromeLogin(user_agent=self.user_agent, headless=self.headless, executable_path=self.driver_path)
        super(Browser, self).__init__(gmail_id=self.gmail_id, gmail_pw=self.gmail_pw)
        self.parser = self

    async def get_login_cookie(self):
        self.chrome.join_page(self._login_url)
        self.chrome.random_driver_delay()
        login_username = self.chrome.xpath('//*[@id="login-username"]')
        self.chrome.random_driver_delay()
        login_password = self.chrome.xpath('//*[@id="password-input"]')
        self.chrome.random_driver_delay()
        login_username.send_keys(self.user_id)
        self.chrome.random_driver_delay()
        login_password.send_keys(self.password)
        self.chrome.random_driver_delay()
        click_login_button = self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/form/div/div[3]/button'
        )
        self.chrome.random_driver_delay()
        click_login_button.click()

        self.chrome.email_delay()

        self.chrome.random_driver_delay()

        code = await self.parser.get_mail()
        pin_list = self.parser.pin_code_parser(code=code)
        self.chrome.random_driver_delay()
        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[1]/div/input'
        ).send_keys(pin_list[0])

        self.chrome.random_driver_delay()

        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[2]/div/input'
        ).send_keys(pin_list[1])

        self.chrome.random_driver_delay()

        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[3]/div/input'
        ).send_keys(pin_list[2])

        self.chrome.random_driver_delay()

        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[4]/div/input'
        ).send_keys(pin_list[3])

        self.chrome.random_driver_delay()

        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[5]/div/input'
        ).send_keys(pin_list[4])

        self.chrome.random_driver_delay()

        self.chrome.xpath(
            '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[2]/div/div[6]/div/input'
        ).send_keys(pin_list[5])
        self.chrome.random_driver_delay()
        self.chrome.email_delay()
        self.chrome.random_driver_delay()
        cookies = dict(ChainMap(*[{index["name"]: index["value"]} for index in self.chrome.get_cookies()]))
        return cookies
