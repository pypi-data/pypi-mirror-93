class TwoFactorAuthenticationEnabled(Exception):
    pass


class LoginVerificationCodeRequired(Exception):
    pass


class InvalidPassword(Exception):
    pass


class CAPTCHARequired(Exception):
    pass
