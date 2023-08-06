import asyncio
from bergen.enums import ClientType
from bergen.wards.graphql.subscription import SubscriptionGraphQLWard
from bergen.logging import setLogging
from bergen.auths.base import BaseAuthBackend
from bergen.wards.base import BaseWard
from bergen.postmans.base import BasePostman
import logging

import nest_asyncio


#nest_asyncio.apply()

logger = logging.getLogger(__name__)
import os


class BaseBergen:


    def __init__(self, auth: BaseAuthBackend, host: str, port: int, protocol = "http", auto_negotiate=True, bind=True, log=logging.INFO, local=None, loop=None,  client_type: ClientType = None, **kwargs) -> None:
        
        try:
            self.loop = loop or asyncio.get_running_loop()
            self.loop_is_running = True
            logger.info("Using provided Async Loop")
        except RuntimeError:
            self.loop = asyncio.get_event_loop()
            self.loop_is_running = False
            logger.info("Created New Eventloop")

        if bind: 
            # We only import this here for typehints
            from bergen.registries.arnheim import set_current_arnheim
            set_current_arnheim(self)


        if log is not False:
            print(r"     _               _          _              ____ _ _            _    ")   
            print(r"    / \   _ __ _ __ | |__   ___(_)_ __ ___    / ___| (_) ___ _ __ | |_  ")
            print(r"   / _ \ | '__| '_ \| '_ \ / _ \ | '_ ` _ \  | |   | | |/ _ \ '_ \| __| ")
            print(r"  / ___ \| |  | | | | | | |  __/ | | | | | | | |___| | |  __/ | | | |_  ")
            print(r" /_/   \_\_|  |_| |_|_| |_|\___|_|_| |_| |_|  \____|_|_|\___|_| |_|\__| ")
            print(r"")
            setLogging(True, log)


        self.local = local if local is not None else os.getenv("ARNHEIM_LOCAL") == "1" 
        if self.local:
            logger.info("Running in Local Mode")

        self.client_type = client_type
        self.auth = auth
        self.token = self.auth.getToken()
        logger.info(" Auhorized!!!!!")

        self.main_ward = SubscriptionGraphQLWard(host=host, port=port, protocol=protocol, token=self.token, loop=self.loop)

        self._transcript = None
        self.identifierDataPointMap = {}
        self.identifierWardMap: dict[str, BaseWard] = {}


        if auto_negotiate == True and not self.loop_is_running: # If we are running in a loop we shouldn't negotiate
            self.negotiate()

        super().__init__()
            

    @property
    def transcript(self):
        assert self._transcript is not None, "We have to negotiate first with our"
        return self._transcript


    def getExtensionSettings(self, extension):
        assert extension in self.transcript.extensions, f"Arnheim seems to have no idea about this Extension {extension}"
        return self.transcript.extensions[extension]


    def getWardForIdentifier(self, identifier):
        assert self._transcript is not None, "We cannot get query Identifiers on Datapoint before having negotiated them"
        if identifier in self.identifierWardMap:
            return self.identifierWardMap[identifier]
        else:
            return self.main_ward


    def registerDatapoints(self, transcript):
        assert transcript.models is not None, "We apparently didnt't get any points"
        
        from bergen.registries.datapoint import get_datapoint_registry
        datapoint_registry = get_datapoint_registry()

        self.identifierDataPointMap = {model.identifier.lower(): model.point for model in transcript.models}
        self.identifierWardMap = {model.identifier.lower(): datapoint_registry.getClientForData(model.point, self.auth) for model in transcript.models}
        logger.info("Succesfully registered Datapoints") 



    def setPostmanFromSettings(self, transcript):
        settings = transcript.postman

        if settings.type == "pika":
            try:
                from bergen.postmans.pika import PikaPostman
                self.postman = PikaPostman(**settings.kwargs, loop=self.loop)
            except ImportError as e:
                logger.error("You cannot use the Pika Postman without installing aio_pika")
                raise e

        elif settings.type == "websocket":
            try:
                from bergen.postmans.websocket import WebsocketPostman
                self.postman = WebsocketPostman(**settings.kwargs, loop=self.loop)
            except ImportError as e:
                logger.error("You cannot use the Websocket Postman without installing websockets")
                raise e

        else:
            raise Exception(f"Postman couldn't be configured. No Postman for type {settings.type}")

        return self.postman

    
    async def negotiate_async(self, client_type=None):
        from bergen.constants import NEGOTIATION_GQL
        
        # We resort escalating to the different client Type protocols
        clientType = client_type or self.client_type or self.auth.getClientType()
        self._transcript = await NEGOTIATION_GQL.run_async(ward=self.main_ward, variables={"clientType": clientType, "local": self.local})
        self.registerTranscript(self._transcript)

        postman = self.setPostmanFromSettings(self._transcript)
        await postman.configure()

    async def disconnect_async(self, client_type=None):
        await self.postman.disconnect()



    def registerTranscript(self, transcript):
        logger.info(f"Successfully Got Protocols")

        if self._transcript:
            self.registerDatapoints(self._transcript)

        logger.info("We established all Proper Clients for the interaction!")
        logger.info("Arnheim Ready!!!!!!!!")



    def negotiate(self, client_type = None):
        from bergen.constants import NEGOTIATION_GQL
        
        # We resort escalating to the different client Type protocols
        clientType = client_type or self.client_type or self.auth.getClientType()
        self._transcript = NEGOTIATION_GQL.run(ward=self.main_ward, variables={"clientType": clientType or self.auth.getClientType(), "local": self.local})
        self.registerTranscript(self._transcript)

        postman = self.setPostmanFromSettings(self._transcript)
        self.loop.run_until_complete(postman.configure())
        


    def getWard(self) -> BaseWard:
        return self.main_ward

    def getPostman(self) -> BasePostman:
        return self.postman

    def _repr_html_(self):
        return f"""
            <p> Arnheim Client <p>
            <table>
                <tr>
                    <td> Connected to </td> <td> {self.main_ward.host} </td>
                </tr>
            </table>



        """


    async def __aenter__(self):
        await self.negotiate_async()
        print(self)


    async def __aexit__(self,*args, **kwargs):
        await self.disconnect_async()

