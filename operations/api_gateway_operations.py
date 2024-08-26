from pulumi_gcp import apigateway

class ApiGatewayOperations:
    def __init__(self):
        pass

    def create_api_gateway(self, name, openapi_spec):
        api = apigateway.Api(name, openapi_spec=openapi_spec)
        return api

    def delete_api_gateway(self, api_id):
        api = apigateway.Api.get(api_id)
        api.delete()
        return api
