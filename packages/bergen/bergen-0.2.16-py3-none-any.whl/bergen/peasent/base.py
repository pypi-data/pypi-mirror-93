

from abc import ABC, abstractmethod
from typing import Union
from bergen.utils import ExpansionError, expandInputs
from bergen.messages.assignation import AssignationMessage
from bergen.schema import Template
from bergen.constants import OFFER_GQL, SERVE_GQL
import logging
import namegenerator
import asyncio
import websockets
from bergen.models import Node
import inspect
import sys
from aiostream import stream


logger = logging.getLogger()

import json


class BaseHelper(ABC):

    def __init__(self, peasent) -> None:
        self.peasent = peasent
        pass

    @abstractmethod
    async def pass_yield(self, message, value):
        pass

    @abstractmethod
    async def pass_progress(self, message, value):
        pass

    @abstractmethod
    async def pass_result(self, message, value):
        pass

    @abstractmethod
    async def pass_exception(self, message, exception):
        pass


class AssignationHelper():

    def __init__(self, peasent_helper: BaseHelper, assignation) -> None:
        self.peasent_helper = peasent_helper
        self.assignation = assignation
        pass


    def progress(self, value):
        self.peasent_helper.pass_progress(self.message, value)



class BasePeasent(ABC):
    ''' Is a mixin for Our Bergen '''
    helperClass = None


    def __init__(self, *args, loop = None, unique_name = None, **kwargs) -> None:
        
        
        self.unique_name = unique_name or namegenerator.gen()
        self.loop = loop or asyncio.get_event_loop()
        self.pods = {}

        self.templates_to_register = []
        self.pods_to_register = []
        self.peasent_helper = self.helperClass(self)
        super().__init__(*args, loop=loop, **kwargs)





    def register(self, node_or_template: Union[Node, Template], **kwargs):


        def real_decorator(function):
            is_coroutine = inspect.iscoroutinefunction(function)
            is_asyncgen = inspect.isasyncgenfunction(function)


            async def wrapper(message: AssignationMessage):
                
                assignation_helper = AssignationHelper(self.peasent_helper, message)
                kwargs = message.data.inputs
                
                if is_coroutine:
                    result = await function(assignation_helper, **kwargs)
                    await self.peasent_helper.pass_result(message, result)

                elif is_asyncgen:
                    yieldstream = stream.iterate(function(assignation_helper, **kwargs))
                    lastresult = None
                    async with yieldstream.stream() as streamer:
                        async for result in streamer:
                            lastresult = result
                            await self.peasent_helper.pass_yield(message, result)

                    await self.peasent_helper.pass_result(message, lastresult)
                
                else:
                    raise NotImplementedError("We do not allow for non async functions right now")
                
            
            wrapper.__name__ = function.__name__

            if isinstance(node_or_template, Node):
                logger.info(f"Registering Template for {node_or_template.name}")
                self.templates_to_register.append({
                    "node": node_or_template,
                    "params": kwargs,
                    "function": wrapper

                })

            if isinstance(node_or_template, Template):
                logger.info(f"Registering Potential Pod for {node_or_template.id}")
                self.pods_to_register.append({
                    "template": node_or_template,
                    "function": wrapper

                })


            return wrapper


        return real_decorator



    async def setup_and_run(self):
        logger.info("Offering Our Services")
        self.peasent = await SERVE_GQL.run_async(ward=self.main_ward, variables = {"name":self.unique_name})
        logger.info("Our Offer was Accesspted")


        async def offer(node: Node, params: dict, function):
            peasent_template = await OFFER_GQL.run_async(ward=self.main_ward, variables= {"node": node.id, "params": params, "peasent": self.peasent.id})
            return (peasent_template, function)

        logger.info("We are registering our functions as potential Templates")
        template_function_set = await asyncio.gather(*[offer(**values) for values in self.templates_to_register])
        self.templateid_function_map = {value[0].id: value[1] for value in template_function_set}
        self.templateid_template_map = {value[0].id: value[0] for value in template_function_set}

        logger.info(f"Following functions have been allowed! {str(self.templateid_function_map)}")

        logger.debug("Configuring")
        await self.configure()





    @abstractmethod
    async def configure(self) -> str:


        raise NotImplementedError("Please overwrite")


    def run(self):

        self.loop.create_task(self.setup_and_run())

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        
        self.loop.run_forever()

