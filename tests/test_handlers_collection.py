from unittest.mock import create_autospec

import pytest

from FreeSpotify_back.ui.handler_collection import Call
from FreeSpotify_back.ui.handler_collection import HandlersCollection



@pytest.fixture()
def handler():
    def _handler(*args, **kwargs):
        pass

    return create_autospec(_handler)


@pytest.fixture()
def handler2():
    def _handler2(*args, **kwargs):
        pass

    return create_autospec(_handler2)


@pytest.fixture()
def handlers_collection():
    return HandlersCollection()


def test_construction():
    assert HandlersCollection()


def test_bind_one_handler(handlers_collection: HandlersCollection, handler):
    handlers_collection.bind_one_handler_to_event(handler, "test event")

    assert handler in handlers_collection.handlers_on_events["test event"]


def test_bind_handlers(handlers_collection: HandlersCollection, handler, handler2):
    handlers_collection.bind_handlers_to_event(
        [handler, handler2],
        "test event"
    )

    assert handler in handlers_collection.handlers_on_events["test event"]
    assert handler2 in handlers_collection.handlers_on_events["test event"]


def test_raise_event(handlers_collection: HandlersCollection, handler):
    handlers_collection.bind_one_handler_to_event(handler, "test event")

    handlers_collection.raise_event("test event")

    assert Call(handler) in handlers_collection.calls_queue


def test_raise_event_with_args(handlers_collection: HandlersCollection, handler):
    handlers_collection.bind_one_handler_to_event(handler, "test event")

    handlers_collection.raise_event("test event", 1, 2)

    assert Call(handler, (1, 2)) in handlers_collection.calls_queue


def test_execute_calls_queue(handlers_collection: HandlersCollection, handler, handler2):
    handlers_collection.bind_handlers_to_event([handler, handler2], "test event")
    handlers_collection.raise_event("test event")

    handlers_collection.execute_calls_queue()

    handler.assert_called_once()
    handler2.assert_called_once()


def test_execute_calls_queue_with_additional_args(
        handlers_collection: HandlersCollection,
        handler,
        handler2
):
    handlers_collection.bind_handlers_to_event(
        [handler, handler2],
        "test event"
    )

    handlers_collection.raise_event("test event")
    handlers_collection.execute_calls_queue(1)

    handler.assert_called_with(1)
    handler2.assert_called_with(1)


def test_execute_calls_queue_and_raise_event_with_args(handlers_collection, handler):
    handlers_collection.bind_one_handler_to_event(handler, "test event")

    handlers_collection.raise_event("test event", "STRING...")
    handlers_collection.execute_calls_queue(1)

    handler.assert_called_with("STRING...", 1)


def test_execute_calls_queue_and_raise_event_with_some_args(handlers_collection, handler):
    handlers_collection.bind_one_handler_to_event(handler, "test event")

    handlers_collection.raise_event("test event", 1, 2, 3)
    handlers_collection.execute_calls_queue(4)

    handler.assert_called_with(1, 2, 3, 4)
