from . import exceptions


class Incidents(object):
    def __init__(self, connection):
        self.connection = connection
