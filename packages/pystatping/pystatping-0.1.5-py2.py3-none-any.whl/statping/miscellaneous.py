from . import exceptions


class Miscellaneous(object):
    def __init__(self, connection):

        self.connection = connection

    def get_details(self):
        response = self.connection.get("")
        return response

    def get_logs(self):
        response = self.connection.get("logs")
        return response
