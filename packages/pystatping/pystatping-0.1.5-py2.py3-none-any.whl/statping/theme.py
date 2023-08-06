from . import exceptions


class Theme(object):
    def __init__(self, connection):
        self.connection = connection
