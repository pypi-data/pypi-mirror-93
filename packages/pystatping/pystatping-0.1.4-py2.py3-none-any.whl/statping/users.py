from . import exceptions


class Users(object):
    def __init__(self, connection):
        self.connection = connection
