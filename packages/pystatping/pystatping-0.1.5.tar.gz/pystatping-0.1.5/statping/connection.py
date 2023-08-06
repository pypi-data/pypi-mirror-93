import requests

from . import exceptions

# class Statping(object):
class StatpingConnection(object):
    def __init__(self, url, token=None, ssl_verify=False):

        base_url = "{}".format(url if url[-1] != "/" else url[:-1])

        self.base_url = base_url
        self.token = token

        # Set headers
        self.headers = {"Content-Type": "application/json"}

        if self.token:
            self.headers.update({"Authorization": self.token})

        # Init connection
        self.session = requests.Session()
        self.session.verify = ssl_verify

    def __request(self, url=None, method="GET", body=None):

        request = requests.Request(
            method=method, headers=self.headers, url=url, json=body
        )
        prepared_request = self.session.prepare_request(request)

        # TODO handle unhappy flow
        response = self.session.send(prepared_request)

        try:
            response_data = response.json()
        except:
            response_data = response.content

        return response.ok, response.status_code, response_data

    def get(self, path):
        url = f"{self.base_url}/api/{path}"
        resp_ok, resp_status, resp_data = self.__request(url=url)

        return resp_data

    def delete(self, path):
        url = f"{self.base_url}/api/{path}"
        resp_ok, resp_status, resp_data = self.__request(url=url, method="DELETE")

        if resp_ok and resp_status == 200:
            return True

        if resp_status == 404:
            raise exceptions.NotFoundException(f"Unable to find object with url {url}")

        return resp_data

    def post(self, path, body):

        if self.token is None:
            raise exceptions.AuthException(
                "An API token is required when posting data."
            )

        url = f"{self.base_url}/api/{path}"
        resp_ok, resp_status, resp_data = self.__request(
            url=url, method="POST", body=body
        )

        return resp_data

    def patch(self, path, body):

        if self.token is None:
            raise exceptions.AuthException(
                "An API token is required when updating (PUT) data."
            )

        url = f"{self.base_url}/api/{path}"
        resp_ok, resp_status, resp_data = self.__request(
            url=url, method="PATCH", body=body
        )

        return resp_data
