from abc import ABC, abstractmethod
from bergen.managers.base import BaseManager
from bergen.query import TypedGQL
from typing import Callable, Dict, Generic, List, TypeVar, Any
import asyncio


ModelType = TypeVar("ModelType")

class ModelConfigurationError(Exception):
    pass

class ModelManager(BaseManager, Generic[ModelType]):

    def __call__(self, model: ModelType, meta) -> Any:
        self.model = model
        self.meta = meta
        return self

    def get_ward(self):
        try:
            identifier = self.model.Meta.identifier
        except Exception as e:
            raise ModelConfigurationError(f"Make soure your Model {self.model.__name__}overwrites Meta identifier: {e}")
        from bergen.registries.arnheim import get_current_arnheim


        return get_current_arnheim().getWardForIdentifier(identifier=identifier)

    def _call_meta(self, attribute, ward=None, **kwargs):
        from bergen.types.utils import parse_kwargs
        method =  getattr(self.meta, attribute, None)
        assert method is not None, f"Please provide the {attribute} parameter in your ArnheimModel meta class for SchemaClass {self.model.__name__} "


        typed_gql: TypedGQL = method(self.model)

        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass
        else:
            if event_loop.is_running():
                return typed_gql.run(ward=ward, variables=parse_kwargs(kwargs))
            else:
                # Spinning up a new event loop just for that?
                event_loop = asyncio.get_event_loop()
                result = event_loop.run_until_complete(typed_gql.run(ward=ward, variables=parse_kwargs(kwargs)))
                return result



    def get(self, ward=None, **kwargs) -> ModelType:
        return self._call_meta("get", ward=ward, **kwargs)
        
    def create(self, ward=None, **kwargs) -> ModelType:
        return self._call_meta("create", ward=ward, **kwargs)

    def filter(self, ward=None, **kwargs) -> List[ModelType]:
        return self._call_meta("filter", ward=ward, **kwargs)

    def update(self, ward=None, **kwargs) -> ModelType:
        return self._call_meta("update", ward=ward, **kwargs)

    def all(self, ward=None) -> List[ModelType]:
        return self._call_meta("filter", ward=ward)