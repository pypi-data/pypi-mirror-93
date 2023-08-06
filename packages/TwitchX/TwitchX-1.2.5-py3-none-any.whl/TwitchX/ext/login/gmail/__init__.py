import re
import email
import imaplib
from email import header
from typing import Optional
from bs4 import BeautifulSoup as bs


class GmailParser:
    def __init__(self, gmail_id: str, gmail_pw: str):
        """"""
        self.server = "imap.gmail.com"
        self.box = "Inbox"

        self.gmail_id = gmail_id
        self.gmail_pw = gmail_pw
        self.session: Optional[imaplib.IMAP4_SSL] = None

    @staticmethod
    def find_encoding_info(txt):
        info = header.decode_header(txt)
        s, encoding = info[0]
        return s, encoding

    @staticmethod
    def pin_code_parser(code: list):
        pin = []
        _pin = pin.append
        for i in str(code[0]):
            _pin(int(i))
        return pin

    def init_connection(self):
        self.session = imaplib.IMAP4_SSL(self.server)
        self.session.login(user=self.gmail_id, password=self.gmail_pw)
        self.session.select(self.box)
        return self.session

    async def get_mail(self):
        self.session = self.init_connection()
        result, data = self.session.search(None, 'ALL')
        for num in reversed(data[0].split()):
            result, data = self.session.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            if email_message["From"] == 'Twitch <account@twitch.tv>':
                subject, encode = self.find_encoding_info(email_message['Subject'])
                if type(subject) == str:
                    print('Subject', subject)
                else:
                    subject.decode(f"{encode}")

                message = ''
                if email_message.is_multipart():
                    for part in email_message.get_payload():
                        if part.get_content_type() == 'text/html':
                            _bytes = part.get_payload(decode=True)
                            encode = part.get_content_charset()
                            message = message + str(_bytes, encode)
                else:
                    if email_message.get_content_type() == 'text/html':
                        _bytes = email_message.get_payload(decode=True)
                        encode = email_message.get_content_charset()
                        message = str(_bytes, encode)
                if message:
                    # print(message)
                    soup = bs(message, "lxml")
                    da = soup.select('table > tbody > tr > th > div')
                    sss = re.findall(r"[0-9]{6}", str(da[0]))
                    return sss
