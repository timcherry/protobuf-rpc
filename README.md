ZeroMQ+Gevent RPC Implementation for Google Protobufs Services
===============================================================

Python library implemenation for GoogleProtobuf Services(RPC). Uses ZeroMQ for transport layer. Server Uses Gevent for threading.

https://developers.google.com/protocol-buffers/docs/proto#services

Requires:
-------------------

1. python2.7
2. Virtualenv 1.11.6
3. protoc 2.5.0 (https://code.google.com/p/protobuf/downloads/list)

Build:
-------------------

```sh
make all
```

Build Protobufs:
-------------------
This is done as part of `make all` but to explicitly build protobufs:

```sh
make pb2_compile
```

Run Test Server:
-------------------

```sh
make test-server
```

Run Test Client:
-------------------

```sh
make test-client
```

Build a python egg:
---------------------

```sh
make package
```
