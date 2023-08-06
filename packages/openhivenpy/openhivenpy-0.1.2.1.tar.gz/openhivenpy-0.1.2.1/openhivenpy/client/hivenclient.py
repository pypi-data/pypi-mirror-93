import asyncio
import sys
import os
import logging
import traceback
import typing
from time import time
from typing import Optional, Union

from openhivenpy.settings import load_env
from openhivenpy.gateway.connection import ExecutionLoop
from openhivenpy.gateway import Connection, HTTP
from openhivenpy.events import EventHandler
import openhivenpy.exceptions as errs
import openhivenpy.utils as utils
import openhivenpy.types as types

__all__ = 'HivenClient'

logger = logging.getLogger(__name__)


def _check_dependencies() -> None:
    pkgs = ['asyncio', 'typing', 'aiohttp']
    for pkg in pkgs:
        if pkg not in sys.modules:
            logger.critical(f"[HIVENCLIENT] Module {pkg} not found in locally installed modules!")
            raise ImportError(f"Module {pkg} not found in locally installed modules!", name=pkg)


class HivenClient(EventHandler):
    """`openhivenpy.client.HivenClient` 
    
    HivenClient
    ~~~~~~~~~~~
    
    Main Class for connecting to Hiven and interacting with the API.
    
    Inherits from EventHandler and API
    
    Parameter:
    ----------
    
    token: `str` - Needed for the authorization to Hiven.
                    Will throw `HivenException.InvalidToken` if length not 128, is None or is empty
    
    restart: `bool` - If set to `True` the process will restart if an error occurred while running the websocket.
                    If the restart failed again the program will stop. Defaults to `False`
    
    client_type: `str` - Automatically set if UserClient or BotClient is used.
                        Raises `HivenException.InvalidClientType` if set incorrectly. Defaults to `BotClient`
    
    event_handler: `openhivenpy.events.EventHandler` - Handler for the events. Can be modified and customized if wanted.
                                                        Creates a new one on Default
    
    heartbeat: `int` - Intervals in which the bot will send life signals to the Websocket. Defaults to `30000`
   
    log_ws_output: `bool` - Will additionally to normal debug information also log the ws responses
    
    close_timeout: `int` -  Seconds after the websocket will timeout after the handshake
                            didn't complete successfully. Defaults to `40`
    
    event_loop: Optional[`asyncio.AbstractEventLoop`] - Event loop that will be used to execute all async functions.
                                                        Defaults to None!
    
    """

    def __init__(
            self,
            token: str,
            *,
            event_handler: Optional[EventHandler] = None,
            client_type: Optional[str] = None,
            **kwargs):

        # Loading the openhivenpy.env variables
        load_env()
        # Calling super to make the client it's own event_handler
        super().__init__(self)

        if client_type == "user":
            self._CLIENT_TYPE = "user"
            self._bot = False

        elif client_type == "bot":
            self._CLIENT_TYPE = "bot"
            self._bot = True

        elif client_type is None:
            logger.warning("[HIVENCLIENT] Client type is None. Defaulting to BotClient.")
            self._CLIENT_TYPE = "bot"
            self._bot = True

        else:
            logger.error(f"[HIVENCLIENT] Expected 'user' or 'bot', got '{client_type}'")
            raise errs.InvalidClientType(f"Expected 'user' or 'bot', got '{client_type}'")

        _user_token_len = int(os.getenv("USER_TOKEN_LEN"))
        _bot_token_len = int(os.getenv("BOT_TOKEN_LEN"))

        if token is None or token == "":
            logger.critical(f"[HIVENCLIENT] Empty Token was passed!")
            raise errs.InvalidToken()

        elif len(token) != _user_token_len and len(token) != _bot_token_len:  # Bot TOKEN
            logger.critical(f"[HIVENCLIENT] Invalid Token was passed!")
            raise errs.InvalidToken()

        _check_dependencies()

        self._TOKEN = token  # Token is const!
        self._event_loop = kwargs.get('event_loop')  # Loop defaults to None!

        if event_handler:
            self.event_handler = event_handler
        else:
            # Using the Client as Event Handler => Using inherited functions!
            self.event_handler = self

        # Websocket and client data are being handled over the Connection Class
        self._connection = Connection(event_handler=self.event_handler,
                                      token=token,
                                      **kwargs)

        # Removed nest_async for now!
        # nest_asyncio.apply(loop=self.loop)

    def __str__(self) -> str:
        return str(getattr(self, "name"))

    def __repr__(self) -> str:
        info = [
            ('type', self._CLIENT_TYPE),
            ('open', self.open),
            ('name', getattr(self.user, 'name')),
            ('id', getattr(self.user, 'id'))
        ]
        return '<HivenClient {}>'.format(' '.join('%s=%s' % t for t in info))

    @property
    def token(self) -> str:
        return getattr(self, '_TOKEN', None)

    @property
    def http(self) -> HTTP:
        return getattr(self.connection, '_http', None)

    @property
    def connection(self) -> Connection:
        return getattr(self, '_connection', None)

    @property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        return getattr(self, '_event_loop', None)

    async def connect(self,
                      *,
                      event_loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop(),
                      restart: bool = False) -> None:
        """`openhivenpy.HivenClient.connect()`
        
        Async function for establishing a connection to Hiven.

        Will run in the current running event_loop and not return unless it's finished!

        :param event_loop: Event loop that will be used to execute all async functions.
                           Defaults to fetching the current loop using asyncio.get_event_loop()!
        :param restart: If set to True the bot will restart if an error is encountered!
        """
        try:
            # Overwriting the event_loop to have the current running event_loop
            self._event_loop = event_loop
            self._connection._event_loop = self._event_loop

            # If the client should restart a task for restart handling will be created
            if restart:
                # Adding the restart handler to the background loop to run infinitely
                # and restart when needed!

                # Note! Restart only works after startup! If the startup fails no restart will be attempted!
                self.connection.execution_loop.add_to_loop(self.connection.handler_restart_websocket)
                self.connection._restart = True

            # Starting the connection to Hiven
            await self.connection.connect(event_loop)

        except KeyboardInterrupt:
            pass

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to establish or keep the connection alive; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}!")
            raise errs.SessionCreateException("Failed to establish HivenClient session! >"
                                              f"{sys.exc_info()[0].__name__}: {e}")

    def run(self,
            *,
            event_loop: Optional[asyncio.AbstractEventLoop] = asyncio.get_event_loop(),
            restart: bool = False) -> None:
        """`openhivenpy.HivenClient.run()`
        
        Standard function for establishing a connection to Hiven

        :param event_loop: Event loop that will be used to execute all async functions.
                           Defaults to fetching the current loop using asyncio.get_event_loop()!
        :param restart: If set to True the bot will restart if an error is encountered!

        """
        try:
            # Overwriting the event_loop to have the current running event_loop
            self._event_loop = event_loop
            self.connection._event_loop = self._event_loop

            # If the client should restart a task for restart handling will be created
            if restart:
                # Adding the restart handler to the background loop to run infinitely
                # and restart when needed!

                # Note! Restart only works after startup! If the startup fails no restart will be attempted!
                self.connection.execution_loop.add_to_loop(self.connection.handler_restart_websocket)
                self.connection._restart = True

            self.event_loop.run_until_complete(self.connection.connect(event_loop))

        except KeyboardInterrupt:
            pass

        except Exception as e:
            utils.log_traceback(level='critical',
                                msg="[HIVENCLIENT] Traceback:",
                                suffix="Failed to establish or keep the connection alive; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}!")
            raise errs.SessionCreateException("Failed to establish HivenClient session! >"
                                              f"{sys.exc_info()[0].__name__}: {e}")

    async def destroy(self, reason: str = "", *, exec_loop=True) -> bool:
        """`openhivenpy.HivenClient.destroy()`
        
        Kills the event loop and the running tasks! 
        
        Will likely throw a RuntimeError if the client was started in a coroutine or if future coroutines
        are going to get executed!

        Parameter
        ~~~~~~~~

        exec_loop: `bool` - If True closes the execution_loop with the other tasks. Defaults to True

        """
        try:
            if self.connection.closed:
                await self.connection.destroy(exec_loop, reason=reason)
                return True
            else:
                logger.error("[HIVENCLIENT] An attempt to close the connection to Hiven failed due to no current active"
                             " Connection!")
                return False

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to close client session and websocket to Hiven; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")
            raise errs.UnableToClose(f"Failed to close client session and websocket to Hiven! > "
                                     f"{sys.exc_info()[0].__name__}: {e}")

    async def close(self, reason: str = "", *, exec_loop=True) -> bool:
        """`openhivenpy.HivenClient.close()`
        
        Stops the current connection and running tasks.
        
        Returns `True` if successful

        Parameter
        ~~~~~~~~

        exec_loop: `bool` - If True closes the execution_loop with the other tasks. Defaults to True

        """
        try:
            if self.connection.closed:
                await self.connection.close(exec_loop, reason=reason)
                return True
            else:
                logger.error("[HIVENCLIENT] An attempt to close the connection to Hiven failed "
                             "due to no current active Connection!")
                return False

        except KeyboardInterrupt:
            pass

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to close client session and websocket to Hiven; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")
            raise errs.UnableToClose(f"Failed to close client session and websocket to Hiven! > "
                                     f"{sys.exc_info()[0].__name__}: {e}")

    @property
    def client_type(self) -> str:
        return getattr(self, '_CLIENT_TYPE', None)

    @property
    def ready(self) -> bool:
        return getattr(self.connection, 'ready', None)

    @property
    def initialised(self) -> bool:
        """`openhivenpy.HivenClient.initialised`

        True if Websocket and HTTP are connected and running

        """
        return getattr(self.connection, 'initialised', None)

    # Meta data
    # -----------
    @property
    def amount_houses(self) -> int:
        return getattr(self.connection, 'amount_houses', None)

    @property
    def houses(self) -> list:
        return getattr(self.connection, 'houses', None)

    @property
    def users(self) -> list:
        return getattr(self.connection, 'users', None)

    @property
    def rooms(self) -> list:
        return getattr(self.connection, 'rooms', None)

    @property
    def private_rooms(self) -> list:
        return getattr(self.connection, 'private_rooms', None)

    @property
    def relationships(self) -> list:
        return getattr(self.connection, 'relationships', None)

    @property
    def house_memberships(self) -> list:
        return getattr(self.connection, 'house_memberships', None)

    # Client data
    # -----------
    @property
    def name(self) -> str:
        return getattr(self.user, 'name', None)

    @property
    def user(self) -> Union[types.User, None]:
        return getattr(self.connection, '_client_user', None)

    # General Connection Properties
    @property
    def connection_status(self) -> str:
        """`openhivenpy.HivenClient.get_connection_status`

        Returns a string with the current connection status.
        
        Can be either 'OPENING', 'OPEN', 'CLOSING' or 'CLOSED'

        """
        return getattr(self.connection, 'connection_status', None)

    @property
    def open(self) -> bool:
        """`openhivenpy.HivenClient.websocket`
        
        Returns `True` if the connection is open
        
        Opposite property to closed
        
        """
        return getattr(self.connection, 'open', None)

    @property
    def closed(self) -> bool:
        """`openhivenpy.HivenClient.closed`

        Returns `True` if the ws connection is closed
        
        Opposite property to open
        
        """
        return getattr(self.connection, 'closed', None)

    @property
    def execution_loop(self) -> ExecutionLoop:
        return getattr(self.connection, 'execution_loop', None)

    @property
    def connection_start(self) -> float:
        """`openhivenpy.HivenClient.connection_start`

        Point of connection start in unix dateformat

        """
        return getattr(self.connection, 'connection_start', None)

    @property
    def startup_time(self) -> float:
        return getattr(self.connection, 'startup_time', None)

    async def edit(self, **kwargs) -> bool:
        """`openhivenpy.HivenClient.edit()`
        
        Change the signed in user's/bot's data. 
        
        Available options: header, icon, bio, location, website.
        
        Alias for HivenClient.connection.edit()
        
        """
        # Connection Object contains inherited Client data => edit() stored there
        return await self.connection.edit(**kwargs)

    async def fetch_room(self, room_id: int) -> Union[types.Room, None]:
        """`openhivenpy.HivenClient.getRoom()`
        
        Returns a cached Hiven Room Object
        
        Warning:
        --------
        
        Data can and will probably be outdated!
        
        Only use this when up-to-date data does not matter or only small checks need to be made on the Room!
        
        Rather consider using get_room()
        
        """
        return utils.get(self.rooms, id=room_id)

    async def fetch_house(self, house_id: int) -> Union[types.House, None]:
        """`openhivenpy.HivenClient.getHouse()`
        
        Returns a cached Hiven Room Object
        
        Warning:
        --------
        
        Data can and will probably be outdated!
        
        Only use this when up-to-date data does not matter or only small checks need to be made on the Room!
        
        Rather consider using get_house()
        
        """
        return utils.get(self.houses, id=house_id)

    async def fetch_user(self, user_id: int) -> Union[types.User, None]:
        """`openhivenpy.HivenClient.getUser()`
        
        Returns a cached Hiven User Object
        
        Warning:
        --------
        
        Data can and will probably be outdated!
        
        Only use this when up-to-date data does not matter or only small checks need to be made on the Room!
        
        Rather consider using get_user()
    
        """
        return utils.get(self.users, id=user_id)

    async def get_house(self, house_id: int) -> Union[types.House, None]:
        """`openhivenpy.HivenClient.get_house()`
        
        Returns a Hiven House Object based on the passed id.
        
        Returns the House if it exists else returns None
        
        """
        try:
            cached_house = utils.get(self.houses, id=house_id)
            if cached_house:
                return cached_house

                # TODO! Needs to be done in the future!
            else:
                return None

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get House based with id {house_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def get_user(self, user_id: int) -> Union[types.User, None]:
        """`openhivenpy.HivenClient.get_user()`
        
        Returns a Hiven User Object based on the passed id.
        
        Returns the House if it exists else returns None
        
        """
        try:
            cached_user = utils.get(self.users, id=user_id)
            if cached_user:
                raw_data = await self.connection.http.request(endpoint=f"/users/{id}")
                if raw_data:
                    data = raw_data.get('data')
                    if data:
                        user = types.User(data, self.connection.http)
                        self.connection._users.remove(cached_user)
                        self.connection._users.append(user)
                        return user
                    else:
                        logger.warning("[HIVENCLIENT] Failed to request user data from the Hiven-API!")
                        return cached_user
                else:
                    logger.warning("[HIVENCLIENT] Failed to request user data from the Hiven-API!")
                    return cached_user
            else:
                return None

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get User based with id {user_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def get_room(self, room_id: int) -> Union[types.Room, None]:
        """`openhivenpy.HivenClient.get_room()`
        
        Returns a Hiven Room Object based on the passed house id and room id.
        
        Returns the Room if it exists else returns None
        
        """
        try:
            cached_room = utils.get(self.rooms, id=room_id)
            if cached_room:
                house = cached_room.house

                raw_data = await self.connection.http.request(endpoint=f"/rooms/{room_id}")
                # Currently not possible to request room data from Hiven!
                # Therefore only cached rooms can be accessed at the moment!
                if raw_data:
                    data = raw_data.get('data')
                    if data:
                        room = types.Room(data, self.connection.http, house)
                        # Appending the data to the client cache
                        self.connection._rooms.remove(cached_room)
                        self.connection._rooms.append(room)
                        return room
                    else:
                        logger.warning("[HIVENCLIENT] Failed to request room data from the Hiven-API!")
                        return cached_room
                else:
                    logger.warning("[HIVENCLIENT] Failed to request room data from the Hiven-API!")
                    return cached_room
            else:
                return None

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get Room with id {room_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def get_private_room(self, room_id: float) -> Union[types.PrivateRoom, None]:
        """`openhivenpy.HivenClient.get_private_room()`
        
        Returns a Hiven `PrivateRoom` or `GroupChatRoom` Object based on the passed house id and room id.
        
        Returns the Room if it exists else returns None
        
        """
        try:
            cached_private_room = utils.get(self.private_rooms, id=room_id)
            if cached_private_room:
                raw_data = await self.connection.http.request(endpoint=f"/rooms/{room_id}")
                # Currently not possible to request room data from Hiven!
                # Therefore only cached rooms can be accessed at the moment!
                if raw_data:
                    data = raw_data.get('data')
                    if data:
                        room = types.PrivateRoom(data, self.connection.http)
                        # Appending the data to the client cache
                        self.connection._private_rooms.remove(cached_private_room)
                        self.connection._private_rooms.append(room)
                        return room
                    else:
                        logger.warning("[HIVENCLIENT] Failed to request private_room data from the Hiven-API!")
                        return cached_private_room
                else:
                    logger.warning("[HIVENCLIENT] Failed to request private_room data from the Hiven-API!")
                    return cached_private_room
            else:
                return None

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get Private Room with id {room_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def create_house(self, name: str) -> types.LazyHouse:
        """`openhivenpy.HivenClient.create_house()`
        
        Creates a new house on Hiven if the limit is not yet reached
        
        Returns a low-level form of the House object!

        Note! The returned house does not have all the necessary data and only the basic data!
        To get the regular house use `utils.get(client.houses, id=house_id)`
        
        """
        try:
            resp = await self.connection.http.post(
                endpoint="/houses",
                json={'name': name})

            if resp.status < 300:
                raw_data = await resp.json()
                if raw_data:
                    data = raw_data.get('data')
                    if data:
                        house = types.LazyHouse(data, self.connection.http)
                        return house
                    else:
                        raise errs.HTTPReceivedNoData()
                else:
                    raise errs.HTTPReceivedNoData()
            else:
                raise errs.HTTPFailedRequest()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to create House; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def delete_house(self, house_id: int) -> Union[int, None]:
        """`openhivenpy.HivenClient.delete_house()`
        
        Deletes a house based on passed id on Hiven
        
        Returns the id of the House if successful
        
        Parameter
        ~~~~~~~~~
        
        house_id: `int` - Id of the house
        
        """
        try:
            cached_house = utils.get(self.houses, id=int(house_id))
            if cached_house:
                resp = await self.connection.http.delete(endpoint=f"/houses/{house_id}")

                if resp.status < 300:
                    return self.user.id
                else:
                    raise errs.HTTPFailedRequest()
            else:
                logger.warning(f"[HIVENCLIENT] The house with id {house_id} does not exist in the client cache!")
                return None

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to delete House; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def fetch_invite(self, invite_code: str) -> Union[types.Invite, None]:
        """`openhivenpy.HivenClient.get_invite()`
        
        Fetches an invite from Hiven
        
        Returns an `Invite` Object
        
        """
        try:
            raw_data = await self.connection.http.request(endpoint=f"/invites/{invite_code}")

            data = raw_data.get('data')
            if data:
                house_data = data.get('house')
                _raw_data = await self.http.request(endpoint=f"/users/{house_data.get('owner_id')}")
                if _raw_data:
                    _data = _raw_data.get('data')
                    if _data:
                        # Creating a house with the data
                        house = types.LazyHouse(
                            data=house_data,
                            http=self.http)
                    else:
                        raise errs.HTTPReceivedNoData()
                else:
                    raise errs.HTTPReceivedNoData()

                return types.Invite(data, house, self.connection.http)
            else:
                raise errs.HTTPReceivedNoData()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to fetch the invite with invite_code '{invite_code}'; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def get_feed(self) -> Union[types.Feed, None]:
        """`openhivenpy.HivenClient.get_feed()`
        
        Get the current users feed
        
        Returns an `Feed` Object
        
        """
        try:
            raw_data = await self.connection.http.request(endpoint=f"/streams/@me/feed")

            if raw_data:
                data = raw_data.get('data')
                if data:
                    return types.Feed(data, self.connection.http)
                else:
                    raise errs.HTTPReceivedNoData()
            else:
                raise errs.HTTPReceivedNoData()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get the users feed; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def get_mentions(self) -> Union[list, types.Mention]:
        """`openhivenpy.HivenClient.get_mentions()`
        
        Gets all mentions of the client user
        
        Returns a list of `Mention` Objects
        
        """
        try:
            raw_data = await self.connection.http.request(endpoint=f"/streams/@me/mentions")

            data = raw_data.get('data')
            if data:
                mention_list = []
                for msg_data in data:
                    author = types.User(msg_data.get('author'), self.connection.http)

                    room = utils.get(self.rooms, id=int(msg_data.get('room_id')))

                    message = types.Message(
                        msg_data,
                        self.connection.http,
                        room.house,
                        room,
                        author)
                    mention_list.append(message)

                return mention_list
            else:
                raise errs.HTTPReceivedNoData()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to get the users mentions; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")

    async def change_room_settings(self, room_id=None, **kwargs) -> Union[types.Room, None]:
        """`openhivenpy.HivenClient.change_room_settings()`
 
        Changed a room settings if permission are sufficient!
        
        Returns the `Room` object if the room exists in the known rooms
 
        Parameter
        ~~~~~~~~~
        
        Only one is required to execute the request!
        
        room_id: `int` - Id of the room that should be modified

        room: `openhivenpy.types.Room` - Room object that should be modified
        
        Available Options
        ~~~~~~~~~~~~~~~~~
        
        notification_preference: `int` - Notification preference for the room. 0 = 'all'/1 = 'mentions'/2 = 'none'
        
        """
        try:
            if room_id is None:
                room = kwargs.get('room')
                try:
                    room_id = room.id
                except Exception:
                    room_id = None

                if room_id is None:
                    logger.warning("Failed to perform request due to missing room_id or room!")
                    return None
            else:
                json = {}
                for key in kwargs:
                    # Searching through the possible keys and adding them if they are found!
                    if key in ['notification_preference', 'name']:
                        json[key] = kwargs.get(key)

                resp = await self.connection.http.put(
                    endpoint=f"/users/@me/settings/room_overrides/{room_id}",
                    json=json)

                if resp.status < 300:
                    return utils.get(self.rooms, id=int(room_id))
                else:
                    raise errs.HTTPFailedRequest()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to edit the room with id {room_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")
            return None

    async def create_private_room(self,
                                  user: typing.Union[int, types.User] = None) -> Union[types.PrivateRoom, None]:
        r"""`openhivenpy.UserClient.create_private_room()`
 
        Adds a user to a private chat room where you can send messages.
        
        Planned: Called when trying to send a message to a user and not room exists yet

        ---

        Only one is required to execute the request! Defaults to user_id if both are provided!

        :param user: User object that should be added to a private room

        :return: The created PrivateRoom if the request was successful else None
        """
        try:
            if type(user) is int:
                user_id = str(user)  # id must be in string format
            elif type(user) is types.User:
                user_id = str(getattr(user, 'id'))  # id must be in string format
            else:
                raise ValueError(f"Expected User or int! Not {type(user)}")

            resp = await self.connection.http.post(endpoint="/users/@me/rooms",
                                                   json={'recipient': user_id})
            if resp.status < 300:
                raw_data = await resp.json()
                data = raw_data.get('data')
                if data:
                    private_room = types.PrivateRoom(data, self.connection.http)
                    # Adding the PrivateRoom to the stored list
                    self.connection._private_rooms.append(private_room)
                    return private_room
                else:
                    raise errs.HTTPReceivedNoData()
            else:
                raise errs.HTTPFailedRequest()

        except Exception as e:
            user_id = user if user is not None else getattr(user, 'id', None)
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to create private_room with user with the id={user_id}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")
            return None

    async def create_private_group_room(self,
                                        recipients: typing.List[typing.Union[int, types.User]] = [],
                                        ) -> Union[types.PrivateGroupRoom, None]:
        """`openhivenpy.UserClient.create_private_group_room()`

        Adds the passed users to a private group chat room where you can send messages.

        Planned: Called when trying to send a message to a user and not room exists yet

        ---

        Only one is required to execute the request! Defaults to user_id if both are provided!

        :param recipients: List of recipients

        :return: The created PrivateGroupRoom if the request was successful else None
        """
        try:
            user_ids = []
            for user in recipients:
                if type(user) is int:
                    user_ids.append(str(user))  # ids must be in string format
                elif type(user) is types.User:
                    user_ids.append(str(getattr(user, 'id')))  # ids must be in string format
                else:
                    raise ValueError(f"Expected User or int! Not {type(user)}")

            resp = await self.connection.http.post(endpoint="/users/@me/rooms", json={'recipients': user_ids})
            if resp.status < 300:
                raw_data = await resp.json()
                data = raw_data.get('data')
                if data:
                    private_room = types.PrivateGroupRoom(data, self.connection.http)
                    # Adding the PrivateGroupRoom to the stored list
                    self.connection._private_rooms.append(private_room)
                    return private_room
                else:
                    raise errs.HTTPReceivedNoData()
            else:
                raise errs.HTTPFailedRequest()

        except Exception as e:
            utils.log_traceback(msg="[HIVENCLIENT] Traceback:",
                                suffix=f"Failed to send a friend request a user with ids={recipients}; \n"
                                       f"{sys.exc_info()[0].__name__}: {e}")
            return None
