

from abc import ABC, abstractmethod
from bergen.messages.allowance import AllowanceMessage
from typing import Union
from bergen.utils import ExpansionError, expandInputs
from bergen.messages.assignation import AssignationMessage
from bergen.schema import AssignationStatus, Template
from bergen.constants import OFFER_GQL, SERVE_GQL
from bergen.peasent.base import BaseHelper, BasePeasent
import logging
import namegenerator
import asyncio
import websockets
from bergen.models import Node
import inspect
import sys

logger = logging.getLogger()


class WebsocketHelper(BaseHelper):

    async def pass_yield(self, message, value):
        message.data.outputs = value
        message.data.status = AssignationStatus.YIELD
        await self.peasent.send_to_connection(message)

    async def pass_progress(self, message, value):
        message.data.status = AssignationStatus.PROGRESS#
        message.data.statusmessage = str(value)
        await self.peasent.send_to_connection(message)
        pass

    async def pass_result(self,message, value):
        message.data.outputs = value
        message.data.status = AssignationStatus.DONE
        await self.peasent.send_to_connection(message)

    async def pass_exception(self,message, exception):
        message.data.status = AssignationStatus.ERROR#
        message.data.statusmessage = str(exception)
        await self.peasent.send_to_connection(message)
        pass

class WebsocketPeasent(BasePeasent):
    helperClass = WebsocketHelper
    ''' Is a mixin for Our Bergen '''

    def __init__(self, *args, host="localhost", port=8000, **kwargs) -> None:
        self.websocket_host = host
        self.websocket_port = port
        self.websocket_protocol = "ws"

        self.pod_template_map = {}

        super().__init__(*args,**kwargs)

    async def configure(self):
        self.incoming_queue = asyncio.Queue()
        await self.startup()
        
    async def startup(self):

        await self.connect_websocket()
        consumer_task = asyncio.create_task(
            self.producer()
        )
        producer_task = asyncio.create_task(
            self.workers()
        )

        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.ALL_COMPLETED
        )
        for task in pending:
            task.cancel()


    async def connect_websocket(self):
        uri = f"{self.websocket_protocol}://{self.websocket_host}:{self.websocket_port}/peasent/{self.unique_name}/?token={self.token}"
        try:
            self.connection = await websockets.client.connect(uri)

            # Our initial payload will be the Pods that were registered! Our allowance

            message = await self.connection.recv()
            allowance = AllowanceMessage.from_channels(message=message)

            self.pod_template_map = allowance.data.pod_template_map
            logger.info(f"We are able to host these pods {[ pod for pod, template in self.pod_template_map.items()]}")



        except ConnectionRefusedError:
            sys.exit('error: cannot connect to backend')


    async def producer(self):
        logger.warning(" [x] Awaiting Node Calls")
        async for message in self.connection:
            await self.incoming_queue.put(message)
        # await self.send_queue.put(message)


    async def send_to_connection(self, message: AssignationMessage):
        await self.connection.send(message.to_channels())




    async def workers(self):
        while True:
            message = await self.incoming_queue.get()
            message = AssignationMessage.from_channels(message)
            assert message.data.pod is not None, "Received assignation that had no Pod?"
            template = self.pod_template_map[message.data.pod]

            logger.info(f"Started Task for Pod {message.data.pod} hosting Node: {message.data.node}")
            asyncio.create_task(self.templateid_function_map[template](message)) # Run in parallel
            self.incoming_queue.task_done()


    

