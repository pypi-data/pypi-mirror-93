import requests

# from . import exceptions
import statping.connection as connection
import statping.miscellaneous as miscellaneous
import statping.services as services
import statping.incidents as incidents
import statping.groups as groups
import statping.users as users
import statping.notifiers as notifiers
import statping.messages as messages
import statping.checkins as checkins
import statping.theme as theme
import statping.oauth as oauth


class Statping(object):
    def __init__(self, url, **kwargs):
        self.connection = connection.StatpingConnection(url, **kwargs)
        self.miscellaneous = miscellaneous.Miscellaneous(self.connection)
        self.services = services.Services(self.connection)
        self.incidents = incidents.Incidents(self.connection)
        self.groups = groups.Groups(self.connection)
        self.users = users.Users(self.connection)
        self.notifiers = notifiers.Notifiers(self.connection)
        self.messages = messages.Messages(self.connection)
        self.checkins = checkins.Checkins(self.connection)
        self.theme = theme.Theme(self.connection)
        self.oauth = oauth.Oauth(self.connection)
