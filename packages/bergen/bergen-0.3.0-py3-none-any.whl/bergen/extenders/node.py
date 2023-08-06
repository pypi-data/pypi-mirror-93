from typing import Any
from bergen.schema import AssignationParams
from bergen.registries.arnheim import get_current_arnheim
import asyncio
from bergen.types.model import ArnheimModel
from bergen.extenders.base import BaseExtender
import logging
from aiostream import stream
import uuid




logger = logging.getLogger(__name__)




class NodeExtender(BaseExtender):


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        
        bergen = get_current_arnheim()

        self._postman = bergen.getPostman()
        self._loop, self._force_sync = bergen.getLoopAndContext()

    async def __call_async(self, inputs: dict, params: AssignationParams, **kwargs):
        
        return await self._postman.assign(self, inputs, params, **kwargs)

    async def __delay_async(self, inputs: dict, params: AssignationParams, **kwargs):
    
        return await self._postman.delay(self, inputs, params, **kwargs)

    def stream(self, inputs: dict, params: AssignationParams = None, **kwargs):

        return stream.iterate(self._postman.stream(self, inputs, params, **kwargs))
    
    def delay(self, inputs: dict, params: AssignationParams = None, **kwargs):
        if self._loop.is_running() and not self._force_sync:
            return self.__delay_async(inputs, params, **kwargs)
        else:
            result = self._loop.run_until_complete(self.__call_async(inputs, params, **kwargs))
            return result


    def __call__(self, inputs: dict, params: AssignationParams = None, **kwargs) -> dict:
        """Call this node (can be run both asynchronously and syncrhounsly)

        Args:
            inputs (dict): The inputs for this Node
            params (AssignationParams, optional): [description]. Defaults to None.

        Returns:
            outputs (dict): The ooutputs of this Node
        """
        if self._loop.is_running() and not self._force_sync:
            return self.__call_async(inputs, params, **kwargs)
        else:
            result = self._loop.run_until_complete(self.__call_async(inputs, params, **kwargs))
            return result


    def _repr_html_(self):
        string = f"{self.name}</br>"

        for input in self.inputs:
            string += "Inputs </br>"
            string += f"Port: {input._repr_html_()} </br>"

        for output in self.outputs:
            string += "Outputs </br>"
            string += f"Port: {output._repr_html_()} </br>"


        return string