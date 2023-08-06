from abc import abstractmethod
from abc import ABC
from bergen.query import  TypedGQL
from typing import TypeVar


T = TypeVar("T")

class BaseWard(ABC):

    def __init__(self, loop=None):
        self.loop = loop

    @abstractmethod
    async def configure(self):
        pass

    @abstractmethod
    def run(self, gql: TypedGQL, variables: dict = {}):
        return gql.cls(**{})

    @abstractmethod
    def run_async(self, gql: TypedGQL, variables: dict = {}):
        return gql.cls(**{})