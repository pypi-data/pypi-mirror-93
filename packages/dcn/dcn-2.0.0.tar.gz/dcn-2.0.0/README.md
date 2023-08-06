# DCN Client
## Setup guide
### Using PyPi
#### Linux and MacOS
```
pip3 install dcn
```
#### Windows
```
pip install dcn
```
### Using github
#### Linux and MacOS
```
git clone https://github.com/draklowell/DCNLibrary && cd DCNLibrary && python3 setup.py install
```
#### Windows
Download client and in downloaded folder run
```
python setup.py install
```
### Dependencies
1. ansicolors ( `1.1.8` )
2. pycryptodome ( `3.9.9` )
## Info
#### Privacy
Connection between two nodes is wrapped by `TLSv1.2` ( without certificate verification ), but packet is opened, and can be read by any user.
#### High-level protocols conflict
To avoid protocol conflicts, we recommend to use `protocol sign`, it is some bytes in begin of packet, that indicate what protocol is using
#### License
[Apache License 2.0](LICENSE)
## Using guide
#### Packet format
```
2 BYTES - Size of packet
16 BYTES - Custom UUID
65520 BYTES - Content
```
Max size of content in packet - `65520` ( `pow(2, 16) - 16` ).

#### Create client
There are two arguments - `friendly_hosts` and `limit_queue`

`friendly_hosts` - known nodes in format ( example: `("1.2.3.4", 300)` ), also it request official nodes, from official tracker

`limit_queue` - max size of queue ( `-1` - unlimited ), recommended `65536`
```python
import dnc
client = dnc.client.Client(friendly_hosts = [], limit_queue = -1)
```
#### Send packet
After generating packet, client sends it to all known nodes. After that, it returns the count of successfully sent copies of the packet and packet hash ( as bytes )
```python
import base64
count, hash = client.send(b"Hello, world!")
print(f"Sended copies of packet: {count}")
print(f"Packet hash ( base64 encoded ): {base64.b64encode(hash).decode()}")
```
Output:
```
Sended copies of packet: 1
Packet hash ( base64 encoded ): oZ/dl88Jbb2CiCCQadpxeQSU/HVpHN3k6A+jAIT8G4k=
```
#### Receive next packet
When the client gets the new massage from the node, client adds the packet to the queue. When we call `client.accept()`, we get the first element of the queue, and then remove it ( we can limit the queue, while initializing client )
```python
import base64
content, hash = client.accept() # or client.next() or next(client)
print(f"Content of packet: {content.decode()}")
print(f"Packet hash ( base64 encoded ): {base64.b64encode(hash).decode()}")
```
Output:
```
Content of packet: Hello world!
Packet hash ( base64 encoded ): oZ/dl88Jbb2CiCCQadpxeQSU/HVpHN3k6A+jAIT8G4k=
```

#### Close client
You need close client in end of work
```python
client.close()
```