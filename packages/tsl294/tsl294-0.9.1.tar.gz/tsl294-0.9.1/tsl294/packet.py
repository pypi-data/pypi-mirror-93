from .crypto.key import Key

from io import BytesIO
from dataclasses import dataclass
import typing

class VerificationFailed(Exception):
    pass

@dataclass
class Packet:

    src: Key
    dst: typing.Union[Key, None]
    sign: bytes
    content: bytes

    @staticmethod
    def check(data: bytes) -> bool:
        return data.startswith(b"TSL294")

    @classmethod
    def fromPacked(cls, data):
        data = BytesIO(data)
        data.read(6)
        
        src = Key.importKey(data.read(294))
        
        dst = data.read(294)
        dst = (None if dst == b"\x00" * 294 else Key.importKey(dst))
        
        sign = data.read(256)
        content = data.read()

        if not src.verify(content, sign):
            raise VerificationFailed("Packet verification failed")
        
        return cls(src, dst, sign, content)

    def getPacked(self):
        return b"TSL294" + self.src.getPublic().exportKey("DER") + (self.dst.getPublic().exportKey("DER") if self.dst else b"\x00" * 294) + self.sign + self.content

    @classmethod
    def new(cls, src: Key, dst: typing.Union[Key, None], data: bytes):
        if dst:
            content = dst.encrypt(data)
        else:
            content = data
        sign = src.sign(content)
        src = src
        return cls(src, dst, sign, content)
