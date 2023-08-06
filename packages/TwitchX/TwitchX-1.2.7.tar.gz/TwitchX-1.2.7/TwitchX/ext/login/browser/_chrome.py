import time
from random import randint
from selenium import webdriver
from selenium.webdriver import ChromeOptions


class ChromeLogin(webdriver.Chrome):
    def __init__(self, user_agent: str, headless: bool = True, executable_path: str = "") -> None:
        self.options = ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("disable-gpu")
        self.options.add_argument("window-size=1920x1080")
        self.options.add_argument("lang=ko_KR")
        self.options.add_argument(f"user-agent={user_agent}")
        self.options.add_argument("Host=www.twitch.tv")

        super().__init__(executable_path=executable_path, options=self.options)
        self.driver = self

    @staticmethod
    def interceptor(request):
        del request.headers["Host"]
        request.headers["Host"] = "www.twitch.tv"

    @staticmethod
    def email_delay():
        num = 30
        time.sleep(num)

    def random_driver_delay(self):
        rand_num = randint(8, 12)
        time.sleep(rand_num)
        self.driver.implicitly_wait(time_to_wait=rand_num)
        del rand_num

    def xpath(self, _xpath: str):
        """Finds an element by xpath."""
        _source = self.driver.find_element_by_xpath(_xpath)
        return _source

    def join_page(self, url):
        self.driver.get(url=url)

