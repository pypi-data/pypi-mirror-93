from . import exceptions


class Checkins(object):
    def __init__(self, connection):
        self.connection = connection
