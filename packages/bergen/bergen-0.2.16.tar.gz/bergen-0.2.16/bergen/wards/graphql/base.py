from abc import ABC

from gql.gql import gql
from bergen.wards.base import BaseWard
from bergen.query import GQL, TypedGQL
from gql.transport.aiohttp import AIOHTTPTransport
import logging
from gql.transport.aiohttp import log as aiohttp_logger
aiohttp_logger.setLevel(logging.WARNING)
import asyncio
from gql import Client, gql

class BaseGraphQLWard(BaseWard, ABC):
    can_subscribe = False
    

    def __init__(self, port=8000, host="localhost", protocol="http", token=None, loop = None) -> None:
        self._graphql_endpoint = f"{protocol}://{host}:{port}/graphql"
        self._token = token
        self._headers = {"Authorization": f"Bearer: {self._token}"}
        
        super().__init__(loop=loop)
