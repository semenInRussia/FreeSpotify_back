import pytest

from my_io.abstract_stream import AbstractStream
from my_io.streams import BasicStream


@pytest.fixture()
def stream():
    return BasicStream()


def test_result(stream: AbstractStream):
    stream.write("Hello my friend")

    assert stream.result == "Hello my friend\n"

def test_listen(stream: AbstractStream):
    assert hasattr(stream, "listen")
