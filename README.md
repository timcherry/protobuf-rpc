async-services (WIP)
====================

This is a transport implementation for Google Protobuf Services:

https://developers.google.com/protocol-buffers/docs/proto#services

It currently uses zeroMQ as transport:

http://zeromq.org/

Build:
-------------------

```sh
make env
```



Build Protobufs:
-------------------

```sh
protoc --proto_path=example/search/ --python_out=example/search/ example/search/SearchService.proto
```
