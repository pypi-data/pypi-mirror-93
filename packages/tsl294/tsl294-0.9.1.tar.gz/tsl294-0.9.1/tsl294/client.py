from func_timeout import func_timeout
from func_timeout.exceptions import FunctionTimedOut
from .packet import Packet
from .crypto.key import Key

import typing
import dcn
import time
import threading

class InvalidKeySize(Exception):
    pass

class Client:
    def __init__(self, key: typing.Union[Key, None] = None, friendly_hosts: list = [], limit_queue = -1):
        if key is None:
            key = Key.random(2048)
        if key.getSize() != 2048:
            raise InvalidKeySize("Key size is not 2048")
        self.key = key
        self.limit_queue = limit_queue
        self.queue = []
        self.dcn_client = dcn.client.Client(friendly_hosts)
        self.running = True
        threading.Thread(target=self._check).start()
    
    def __next__(self):
        while len(self.queue) == 0:
            continue
        data = self.queue[0]
        del self.queue[0]
        return data

    def next(self):
        return next(self)

    def accept(self):
        return next(self)

    def send(self, data: bytes, dst: typing.Union[Key, None]):
        packet = Packet.new(self.key, dst, data)
        return self.dcn_client.send(packet.getPacked())
    
    def _parse(self):
        try:
            data, hash = func_timeout(0.1, self.dcn_client.accept)
        except FunctionTimedOut:
            return
        try:
            if not Packet.check(data):
                return
            packet = Packet.fromPacked(data)
            if packet.dst not in [self.key.getPublic(), None]:
                return
            if packet.dst == None:
                content = packet.content
            else:
                content = self.key.decrypt(packet.content, None)
                if content is None:
                    return
            self.queue.append((content, packet.src, hash))
        except Exception as e:
            return
        if len(self.queue) > self.limit_queue and self.limit_queue >= 0:
            del self.queue[0]

    def _check(self):
        while self.running:
            self._parse()
    def close(self):
        self.running = False
        time.sleep(0.2)
        self.dcn_client.close()