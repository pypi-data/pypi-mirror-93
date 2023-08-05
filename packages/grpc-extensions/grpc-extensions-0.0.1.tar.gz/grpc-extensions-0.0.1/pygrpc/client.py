from __future__ import print_function
import grpc
from grpc import (
    Channel,
    StreamStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    UnaryUnaryClientInterceptor,
)
from typing import Optional, Callable, List, Union

type_client_inspectors = Optional[
    List[
        Union[
            StreamStreamClientInterceptor,
            StreamUnaryClientInterceptor,
            UnaryStreamClientInterceptor,
            UnaryUnaryClientInterceptor,
        ]
    ]
]
default_interceptors: type_client_inspectors = []


def start_client(
    uri: str,
    register: Callable[[Channel], None],
    interceptors: type_client_inspectors = None,
    secure: bool = False,
    crt: str = None,
):
    if not interceptors:
        interceptors = default_interceptors
    if secure and not crt:
        raise Exception("secure mode need crt")
    if secure:
        return run_secure(uri, crt, interceptors, register)
    return run_insecure(uri, interceptors, register)


def run_secure(
    uri: str,
    crt: str,
    interceptors: type_client_inspectors,
    register: Callable[[Channel], None],
):
    with open(crt, "rb") as f:
        credentials = grpc.ssl_channel_credentials(f.read())
    with grpc.secure_channel(uri, credentials) as channel:
        channel = grpc.intercept_channel(channel, *interceptors)
        client = register(channel)
    return client


def run_insecure(uri: str, interceptors, register: Callable[[Channel], None]):
    with grpc.insecure_channel(uri) as channel:
        channel = grpc.intercept_channel(channel, *interceptors)
        client = register(channel)
    return client
