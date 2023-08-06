from requests.exceptions import ConnectionError

# class ConnectionError(ConnectionError):


class ClientError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.status_code = args[1]
        else:
            self.message = None
            self.status_code = 401

    @property
    def response(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class QueryError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.status_code = args[1]
        else:
            self.message = None
            self.status_code = 404

    @property
    def response(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class P2PError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.status_code = args[1]
        else:
            self.message = None
            self.status_code = 404

    @property
    def response(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class AccountError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.status_code = args[1]
        else:
            self.message = None
            self.status_code = 404

    @property
    def response(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class WalletError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.status_code = args[1]
        else:
            self.message = None
            self.status_code = 404

    @property
    def response(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }
