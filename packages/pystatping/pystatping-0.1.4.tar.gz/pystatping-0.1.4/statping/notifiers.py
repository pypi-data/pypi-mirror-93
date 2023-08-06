from . import exceptions


class Notifiers(object):
    def __init__(self, connection):
        self.connection = connection
