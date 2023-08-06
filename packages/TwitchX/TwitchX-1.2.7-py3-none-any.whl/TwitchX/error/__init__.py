class NotSupportBrowser(Exception):
    pass


class MissingClientId(NotImplementedError):
    """Missing Client-ID"""
    pass


class RequiredQueryParameters(NotImplementedError):
    pass
