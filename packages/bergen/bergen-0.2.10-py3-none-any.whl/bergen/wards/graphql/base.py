from abc import ABC

from gql.gql import gql
from bergen.wards.base import BaseWard
from bergen.query import GQL, TypedGQL
from gql.transport.aiohttp import AIOHTTPTransport
import logging
from gql.transport.aiohttp import log as aiohttp_logger
aiohttp_logger.setLevel(logging.WARNING)



class BaseGraphQLWard(BaseWard, ABC):
    can_subscribe = False
    

    def __init__(self, port=8000, host="localhost", protocol="http", token=None, loop = None) -> None:
        self._graphql_endpoint = f"{protocol}://{host}:{port}/graphql"
        self._token = token
        self._headers = {"Authorization": f"Bearer: {self._token}"}
        
        super().__init__(loop=loop)


    async def configure(self):
        self.transport = AIOHTTPTransport(url=self._graphql_endpoint, headers=self._headers)
        self.session = await self.transport.connect()


    def run(self, the_query: TypedGQL, variables: dict = {}, **kwargs):
        return self.loop.run_until_complete(self.run_async(the_query, variables=variables, **kwargs))

    async def run_async(self, the_query: TypedGQL, variables: dict = {}, **kwargs):
        
        query_node = gql(the_query.query)
        response = await self.transport.execute(query_node, variable_values=variables)
        return the_query.extract(response.data)