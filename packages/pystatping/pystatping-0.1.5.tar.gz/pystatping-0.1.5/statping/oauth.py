from . import exceptions


class Oauth(object):
    def __init__(self, connection):
        self.connection = connection
