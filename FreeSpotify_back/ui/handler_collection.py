from collections.abc import Callable
from typing import NamedTuple

Handler = Callable


class Call(NamedTuple):
    """A representation of a call that will be executed later sometime later."""

    callback: Callable
    args: tuple = ()
    kwargs: dict = {}

    def execute(
        self, *additional_args, **additional_kwargs  # noqa: ANN002
    ) -> None:  # noqa: ANN003
        """Execute the call.

        Notice that the call can't return a value (it's a dirty function)
        """
        args = self.args + additional_args
        kwargs = dict(**additional_kwargs, **self.kwargs)
        self.callback(*args, **kwargs)


class AsyncCall(NamedTuple):
    """It likes a `Call` (see above), but asynchronously."""

    callback: Callable
    args: tuple = ()
    kwargs: dict = {}

    async def execute(
        self, *additional_args, **additional_kwargs  # noqa: ANN002
    ) -> None:  # noqa: ANN003
        """Execute the call.

        Notice that the call can't return a value (it's a dirty function)
        """
        args = self.args + additional_args
        kwargs = dict(**additional_kwargs, **self.kwargs)
        await self.callback(*args, **kwargs)


class HandlersCollection:
    """A compostion of `Call`s."""

    CurrentCallType = Call

    def __init__(self):
        """Build a new handles collection with empty call queue."""
        self._calls_queue: list[Call] = []
        self._handlers_on_events: dict[str, list[Handler]] = {}

    @property
    def handlers_on_events(self) -> dict[str, list[Handler]]:
        """Dict of event names and their handlers."""
        return self._handlers_on_events

    @property
    def calls_queue(self) -> list[CurrentCallType]:
        """Queue of `Call`s."""
        return self._calls_queue

    def new_handler(self, event_name: str):  # noqa: ANN201
        """A decorator to bind a function with event."""  # noqa: D401

        def wrapper(func):  # noqa: ANN202, ANN001
            self.bind_one_handler_to_event(func, event_name)
            return func

        return wrapper

    def bind_handlers_to_event(self, handlers: list[Handler], event_name: str) -> None:
        """Bind some handlers with a given event."""
        for handler in handlers:
            self.bind_one_handler_to_event(handler, event_name)

    def bind_one_handler_to_event(self, handler: Handler, event_name: str) -> None:
        """Bind a handler with a given event."""
        if not self.handlers_on_events.get(event_name):
            self._handlers_on_events[event_name] = []

        self._handlers_on_events[event_name].append(handler)

    def is_has_handlers_on_events(self, event_name: str) -> bool:
        """Return True, when an event has handlers."""
        return bool(self._handlers_on_events.get(event_name))

    def raise_event(
        self,  # noqa: D102, ANN201
        event_name: str,
        *handlers_args,  # noqa: ANN002
        **handlers_kwargs
    ):  # noqa: ANN003
        handlers_of_current_event = self._handlers_on_events[event_name]

        new_calls = [
            self.CurrentCallType(callback, args=handlers_args, kwargs=handlers_kwargs)
            for callback in handlers_of_current_event
        ]

        self._extend_calls_queue(new_calls)

    def _extend_calls_queue(self, calls: list) -> None:
        self._calls_queue.extend(calls)

    def execute_calls_queue(
        self, *additional_args, **additional_kwargs  # noqa: ANN002
    ) -> None:  # noqa: ANN003
        """Execute each call from the queue."""
        for _ in range(len(self._calls_queue)):
            self.execute_last_call_from_queue(*additional_args, **additional_kwargs)

    def execute_last_call_from_queue(
        self, *additional_args, **additional_kwargs  # noqa: ANN002
    ) -> None:  # noqa: ANN003
        """Execute the last call from the queue."""
        last_call = self._calls_queue.pop()
        last_call.execute(*additional_args, **additional_kwargs)


class AsyncHandlersCollection(HandlersCollection):
    """It likes a `HandlersCollection` (see above), but asynchronously."""

    CurrentCallType = AsyncCall

    def __init__(self):
        """Build a new handles collection with empty call queue."""
        super().__init__()
        self._calls_queue: list[AsyncCall] = []

    async def execute_calls_queue(self, *additional_args, **additional_kwargs) -> None:
        """Execute each call from the queue."""
        await self.execute_last_call_from_queue(*additional_args, **additional_kwargs)

    async def execute_last_call_from_queue(
        self, *additional_args, **additional_kwargs
    ) -> None:
        """Execute the last call from the queue."""
        last_call = self._calls_queue.pop()
        await last_call.execute(*additional_args, **additional_kwargs)
