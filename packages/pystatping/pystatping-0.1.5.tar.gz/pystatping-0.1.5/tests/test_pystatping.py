import sys
import os

import pytest
from ruamel.yaml import YAML

from statping import Statping

STATPING_URL = os.getenv("STATPING_URL", "http://localhost:8088")
STATPING_TOKEN = os.getenv("STATPING_TOKEN", None)
STATPING_SERVICES_FILE = os.getenv("STATPING_SERVICES_FILE", "services.yml")


def load_services(path):
    """Loads statping services from a Yaml file. The format is equal to the bulk input.

    Yields:
        dict: Statping service definition
    """

    with open(path, "r") as yaml_file:

        yaml = YAML(typ="safe")  # default, if not specfied, is 'rt' (round-trip)
        data = yaml.load(yaml_file)

        # Load the service definitions
        services = data["services"]
        # Return a generator containing services to be created
        for service in services:
            yield service


@pytest.fixture
def statping():
    return Statping(
        STATPING_URL,
        token=STATPING_TOKEN,
    )


@pytest.fixture
def service():

    return {
        "name": "New Service",
        "domain": "https://statping.com",
        "expected": "",
        "expected_status": 200,
        "check_interval": 30,
        "type": "http",
        "method": "GET",
        "post_data": "",
        "port": 0,
        "timeout": 30,
        "order_id": 0,
    }


@pytest.mark.skip()
def test_ruamel():

    with open("services.yml", "r") as data:

        yaml = YAML(typ="safe")  # default, if not specfied, is 'rt' (round-trip)
        services_def = yaml.load(data)
        services = services_def["services"]

        for service in services:
            print(service)

        yaml.dump(services, sys.stdout)

        print(yaml)


@pytest.mark.skip()
def test_create_service(service, statping):

    services = load_services(STATPING_SERVICES_FILE)
    for service in services:
        statping.services.create_service(service)


def test_all_services(statping):

    services = statping.services.get_all_services()
    assert type(services) == list


def test_get_services_by_name(statping):

    services = statping.services.get_service_by_name("SC Identity (Keystone)")
    assert len(list(services)) > 0


def test_upsert_service(service, statping):

    services = statping.services.upsert_service(service)


def test_update_service(service, statping):

    service = statping.services.update_service(12, service)


def test_delete_service(service, statping):

    service = statping.services.create_service(service)
    service_id = service["id"]

    statping.services.delete_service(service_id)


def test_get_details(statping):

    assert type(statping.miscellaneous.get_details()) == dict
