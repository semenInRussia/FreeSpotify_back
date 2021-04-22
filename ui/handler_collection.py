from typing import Dict, Callable, List, NamedTuple

Handler = Callable


class Call(NamedTuple):
    callback: Callable
    args: tuple = tuple()
    kwargs: dict = dict()

    def execute(self, *additional_args, **additional_kwargs):
        args = additional_args + self.args
        kwargs = dict(
            **additional_kwargs,
            **self.kwargs
        )

        self.callback(*args, **kwargs)


class HandlersCollection:
    _calls_queue: List[Call] = []
    _handlers_on_events: Dict[str, List[Handler]] = {}

    @property
    def handlers_on_events(self) -> Dict[str, List[Handler]]:
        return self._handlers_on_events

    @property
    def calls_queue(self) -> List[Call]:
        return self._calls_queue

    def handler(self, event_name: str):
        def wrapper(func):
            self.bind_one_handler_to_event(func, event_name)

            return func

        return wrapper

    def bind_handlers_to_event(self, handlers: List[Handler], event_name: str):
        for handler in handlers:
            self.bind_one_handler_to_event(handler, event_name)

    def bind_one_handler_to_event(self, handler: Handler, event_name: str):
        if not self.handlers_on_events.get(event_name):
            self._handlers_on_events[event_name] = []

        self._handlers_on_events[event_name].append(handler)

    def raise_event(self, event_name: str, *handlers_args, **handlers_kwargs):
        handlers_of_current_event = self._handlers_on_events[event_name]

        new_calls = list(map(
            lambda callback: Call(callback, args=handlers_args, kwargs=handlers_kwargs),

            handlers_of_current_event
        ))

        self._extend_calls_queue(new_calls)

    def _extend_calls_queue(self, call: List[Call]):
        self._calls_queue.extend(call)

    def execute_calls_queue(
            self,
            *additional_args,
            **additional_kwargs
    ):
        for _ in range(len(self._calls_queue)):
            self.execute_last_call_from_queue(
                *additional_args,
                **additional_kwargs
            )

    def execute_last_call_from_queue(self, *additional_args, **additional_kwargs):
        last_call = self._calls_queue.pop()

        last_call.execute(*additional_args, **additional_kwargs)
