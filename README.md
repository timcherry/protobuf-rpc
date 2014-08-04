ZeroMQ+Gevent RPC Implementation for Google Protobufs Services
===============================================================

Python implemenation of GoogleProtobuf Services(RPC). Uses ZeroMQ for transport layer. Server uses Gevent for threading.

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



Performance Results:
---------------------
Ping-Pong hammer tests for 10K requets.

Environment: EC2, c1.medium instance, ubuntu-precise image:

HTTP:

	Total Elapsed time (sec): 24.0618028641
	Average Request time (ms): 2.40618028641

RPC Direct Connections:

	Total Elapsed time (sec): 2.44900202751
	Average Request time (ms): 0.244900202751

RPC with ELB:

	Total Elapsed time (sec): 3.47903800011
	Average Request time (ms): 0.347903800011
