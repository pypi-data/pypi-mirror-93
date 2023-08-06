<img src="https://raw.githubusercontent.com/draklowell/TSL294/main/header.png">

Based on [DCN](https://github.com/draklowell/DCNLibrary/)

## Setup guide
### Using PyPi
#### Linux and MacOS
```
pip3 install tsl294
```
#### Windows
```
pip install tsl294
```
### Using github
#### Linux and MacOS
```
git clone https://github.com/draklowell/TSL294 && cd TSL294 && python3 setup.py install
```
#### Windows
Download client and in downloaded folder run
```
python setup.py install
```
### Dependencies
1. dcn ( `2.0.0.4.1.2` )
2. func-timeout ( `4.3.5` )
## Info
#### Privacy
Connection between two nodes is wrapped by `TLSv1.2` ( without certificate verification ), also packets are encrypted with RSA.
#### High-level protocols conflict
To avoid protocol conflicts, we recommend to use `protocol sign`, it is some bytes in begin of packet, that indicate what protocol is using
#### License
[Apache License 2.0](LICENSE)
## Using guide
#### Packet format
```
18 BYTES - DCN Header
844 BYTES - TSL294 Header:
    294 BYTES - Source key ( Can be only RSA key )
    294 BYTES - Destination key ( Can be RSA key or zero bytes - broadcast to all clients)
    256 BYTES - Signature of encrypted content 
64676 BYTES - Encrypted ( if destination is RSA key ) content
```
Max size of content in packet - `64676` ( `pow(2, 16) - 16 - 844` ).

#### Create client
There are three arguments - `key`, `friendly_hosts` and `limit_queue`

`key` - client RSA key ( only `2048 bits` size )

`friendly_hosts` - known nodes in format ( example: `("1.2.3.4", 300)` ), also it request official nodes, from official tracker

`limit_queue` - max size of queue ( `-1` - unlimited ), recommended `65536`
```python
import tsl294
client = tsl294.client.Client(key = tsl294.crypto.key.Key.random(2048), friendly_hosts = [], limit_queue = -1)
```
#### Send packet
After generating packet, client sends it to user with known key. After that, it returns the count of successfully sent copies of the packet and packet hash ( as bytes )
```python
import base64

# Load key from file
with open("target.pem", "rb") as file:
    key = tsl294.crypto.key.Key.importKey(file.read())

# Send packet
count, hash = client.send(b"Hello, world!", key)
print(f"Sended copies of packet: {count}")
print(f"Packet hash ( base64 encoded ): {base64.b64encode(hash).decode()}")
```
Output:
```
Sended copies of packet: 1
Packet hash ( base64 encoded ): L/78pQALheezMsoc9BTxfheAcNIw7fPQtYHsDBjwDSU=
```
#### Receive next packet
When the client gets the new massage from the server, client adds the packet to the queue. When we call `client.accept()`, we get the first element of the queue, and then remove it ( we can limit the queue, while initializing client )
```python
import base64

content, key, hash = client.accept() # or client.next() or next(client)
print(f"Content of packet: {content.decode()}")
print(f"Source of packet: {base64.b64encode(key.getHash()).decode()}")
print(f"Packet hash ( base64 encoded ): {base64.b64encode(hash).decode()}")
```
Output:
```
Content of packet: Hello, world!
Source of packet: MEtdj9sSPdM0g00Hk6q1Jjvx72f53Gd4uIkMYWN4Khk=
Packet hash ( base64 encoded ): L/78pQALheezMsoc9BTxfheAcNIw7fPQtYHsDBjwDSU=
```

#### Close client
You need close client in end of work
```python
client.close()
```

## Simple app
Now, we can create a simple app using `DCN-TSLv294`, which allows to convert user's message to uppercase. When server gets new packet from the user, it converts packet content to uppercase and sends it back to the client. Example:
User sends `Hello, world!`
Server returns `HELLO, WORLD!`
#### Server side
```python
from tsl294.client import Client
from tsl294 import Key

with open("private.pem", "rb") as file:
    key = Key.importKey(file.read())

client = Client(key)

try:
    while True:
        data, key, hash = client.accept()
        client.send(data.upper(), key)
except KeyboardInterrupt:
    pass
client.close()
```
To close server, just press `Ctrl + C`
#### Client side
```python
from tsl294.client import Client
from tsl294 import Key

with open("public.pem", "rb") as file:
    server_key = Key.importKey(file.read())

message = input().encode("utf-8")

client = Client()
try:
    client.send(message, server_key)
    data, key, hash = client.accept()
    while key != server_key.getPublic():
        data, key, hash = client.accept()
    
    print(data.decode("utf-8"))
except KeyboardInterrupt:
    pass
client.close()
```