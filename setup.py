from setuptools import setup, find_packages
import os

base = os.path.dirname(__file__)
local = lambda x: os.path.join(base, x)


def read(fname):
    return open(local(fname)).read()

setup(
    name="protobuf_rpc",
    version="0.1.6",
    author="Tim Cherry",
    author_email="timcherry21@gmail.com",
    description=("Gevent+ZMQ RPC Implementation for Google Protobufs."),
    packages=find_packages(exclude=['tests']),
    long_description="",
    install_requires=["protobuf>=2.5.0",
                      "gevent>=1.0",
                      "pyzmq>=14.3.0"],
    setup_requires=[], # use the requirements.txt file
    test_suite='nose.collector',
    classifiers=[],
)

