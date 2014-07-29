ZeroMQ+Gevent RPC Implementation for Google Protobufs Services
===============================================================

This is a collection of transport implementations for Google Protobuf Services:

https://developers.google.com/protocol-buffers/docs/proto#services

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
