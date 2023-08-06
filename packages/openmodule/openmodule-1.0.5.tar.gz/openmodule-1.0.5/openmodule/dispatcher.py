import logging
from collections import defaultdict
from typing import Union, Optional, Callable, DefaultDict, List, Dict, TypeVar, Type

import zmq
from pydantic import ValidationError, BaseModel

from openmodule.models import ZMQMessage


class Listener:
    def __init__(self, message_class: Type[ZMQMessage], filter: Optional[Dict], handler: Callable):
        self.filter = filter
        self.handler = handler
        self.message_class = message_class

    def matches(self, message: Dict):
        if self.filter is None:
            return True
        else:
            return message.items() >= self.filter.items()


class EventListener(list):
    log: Optional[logging.Logger]

    def __init__(self, *args, log=None):
        super().__init__(*args)
        self.log = log or logging

    def __call__(self, *args, **kwargs):
        for f in self:
            try:
                f(*args, **kwargs)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                self.log.exception(e)


T = TypeVar('T', bound=ZMQMessage)


class MessageDispatcher:
    def __init__(self, name=None):
        """
        :param name: optionally name the dispatcher for logging purposes
        """
        self.name = name
        self.log = logging.getLogger(f"{self.__class__.__name__}({self.name})")
        self.listeners: DefaultDict[bytes, List[Listener]] = defaultdict(list)

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[T],
                         handler: Callable[[T], None], *,
                         filter: Optional[Dict] = None):
        if hasattr(topic, "encode"):
            topic = topic.encode()
        self.listeners[topic].append(Listener(message_class, filter, handler))

    def dispatch(self, topic: bytes, message: Union[Dict, BaseModel]):
        if isinstance(message, BaseModel):
            message = message.dict()

        listeners = self.listeners.get(topic, [])
        for listener in listeners:
            if listener.matches(message):
                self.execute(listener, message)

    def execute(self, listener: Listener, message: Dict):
        try:
            parsed_message = listener.message_class(**message)
        except ValidationError:
            self.log.exception("Invalid message received")
        else:
            try:
                listener.handler(parsed_message)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                self.log.exception("Error in message handler")


class SubscribingMessageDispatcher(MessageDispatcher):
    def __init__(self, subscribe: Callable[[bytes], None], name=None):
        super().__init__(name=name)
        self.subscribe = subscribe

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[T],
                         handler: Callable[[T], None], *,
                         filter: Optional[Dict] = None):
        self.subscribe(topic)
        return super().register_handler(topic, message_class, handler, filter=filter)
