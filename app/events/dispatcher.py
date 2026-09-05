from asyncio import create_task
from collections.abc import Awaitable, Callable

from app.events.models import Event

# define handler
Handler = Callable[[Event], Awaitable[None]]


class Dispatcher:
    def __init__(self) -> None:
        self.registry: dict[type[Event], list[Handler]] = {}

    def subscribe(
        self,
        event_type: type[Event],
        handler: Handler,
    ) -> None:
        self.registry.setdefault(event_type, []).append(handler)

    async def _wrapper(
        self,
        event: Event,
        handler: Handler,
    ) -> None:
        try:
            await handler(event)
        except Exception as error:  # noqa: BLE001
            print(f"handler {handler} failed on {event}: {error}")

    def publish(self, event: Event) -> None:
        handlers = self.registry.get(type(event), [])
        for handler in handlers:
            create_task(self._wrapper(event, handler))
