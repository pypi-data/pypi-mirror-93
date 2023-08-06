import requests
import json
import dataclasses
from pyvise.graphy.base import get_logger
from pyvise.configuration import get_setting

logger = get_logger(__name__)


class GraphyException(Exception):
    pass


@dataclasses.dataclass
class GraphQLQuery:
    query: str = None
    # query_variables: dict = {}

    def generate_json(self, query_variables={}):
        return json.dumps({'query': self.query, 'variables': query_variables})

    def get_headers(self, secret=get_setting('HASURA_SECRET')):
        return {
            'content-type': 'application/json',
            'x-hasura-admin-secret': secret
        }


class GraphQLAPIClient:
    """
    Client transforms hasura responses to python code, throwing exceptions for errors
    """

    def __init__(self, endpoint: str = get_setting('HASURA_ENDPOINT'), secret: str = get_setting('HASURA_SECRET')):
        self.endpoint = endpoint
        self.secret = secret
        self.logger = get_logger(__name__)

    def execute_single_query(self, graphql_query: GraphQLQuery, query_variables: dict):
        response = requests.post(
            self.endpoint,
            headers=graphql_query.get_headers(self.secret),
            data=graphql_query.generate_json(query_variables=query_variables)
        )

        if(response.ok):
            response_message = response.json()

            if response_message.get('errors') is None:
                self.logger.info("GraphQL Response returned")
                return response_message.get('data')
            else:
                errors = response_message.get('errors')
                error_message = f'GraphQL returned an error! Server message: {errors}'
                self.logger.info(error_message, response_message)
                raise Exception(error_message, response_message)
        else:
            error_message = f"HTTP Exception {response.status_code}"
            self.logger.error(error_message)
            raise GraphyException(error_message, response)

    def execute_query(self, graphql_query: GraphQLQuery, operation_name, query_variables: dict):
        raise NotImplementedError("This hasn't been implemented yet")
        # TODO: Add operation name to JSON generation multi_query = query_variables

        response = requests.post(
            self.endpoint,
            headers=graphql_query.get_headers(self.secret),
            data=graphql_query.generate_json(query_variables=query_variables)
        )

        if(response.status_code != 200):
            response_message = response.json()

            if response_message.get('errors') is None:
                self.logger.info("GraphQL Response returned")
                return response_message.get('data')
            else:
                errors = response_message.get('errors')
                error_message = f'GraphQL returned an error! Server message: {errors}'
                self.logger.info(error_message, response_message)
                raise Exception(error_message, response_message)
        else:
            error_message = f"HTTP Exception {response.status_code}"
            self.logger.error(error_message, response)
            raise Exception(error_message, response)
