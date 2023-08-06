from . import exceptions


class Services:
    def __init__(self, connection):

        self.connection = connection

    def create_service(self, service):

        path = "services"
        response = self.connection.post(path, service)

        return response

    def get_all_services(self):
        path = "services"
        response = self.connection.get(path)

        return response

    def get_service(self, service_id):
        """Get a service by it's ID

        Args:
            service_id (int): ID of the service

        Returns:
            dict: Service definition
        """
        path = f"services/{service_id}"
        response = self.connection.get(path)

        return response

    def update_service(self, service_id, service):
        path = f"services/{service_id}"

        response = self.connection.post(path, service)

        return response

        # Check for id in service definition

    def get_service_by_name(self, name):
        """Return a filtered list of services by name"""
        all_services = self.get_all_services()
        for service in all_services:
            if name in service["name"]:
                yield service

    def upsert_service(self, service):
        """Attempt to create or update a service. Uses the name of the
        service to find an existing service. If multiple are found the operation
        is cancelled. Otherwise the service is updated or created.


        Args:
            service (dict): Service definition to upsert.

        Returns:
            dict: Service definition
        """

        ## Try to find the service
        services = list(self.get_service_by_name(service["name"]))
        if len(services) > 1:
            raise exceptions.UpsertException(
                f"Found {len(services)} services by name: {service['name']}, where only one is expected."
            )

        # The service does not exist
        if len(services) == 0:
            # TODO:
            # Attempt to create the service
            new_service = self.create_service(service)
            return new_service

        # The service exists, attempt to update
        if len(services) == 1:

            service_id = services[0]["id"]
            updated_service = self.update_service(service_id, service)

            return updated_service

        raise exceptions.UpsertException(
            "Error handling the response from the get_service_by_name method."
        )

    def delete_service(self, service_id):
        """Delete service by id

        Args:
            service_id (int): ID of the service
        """

        response = self.connection.delete(f"services/{service_id}")
        return response
