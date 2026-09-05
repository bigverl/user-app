import asyncio

from app.events.dispatcher import Dispatcher
from app.events.models import Event, UserCreatedEvent


def _publish_and_run(dispatcher: Dispatcher, event: Event) -> None:
    async def run():
        dispatcher.publish(event)
        await asyncio.sleep(0)

    asyncio.run(run())


class TestSubscribe:
    def test_first_subscriber_is_added_to_a_new_list(self, dispatcher):
        async def handler(event):
            pass

        dispatcher.subscribe(UserCreatedEvent, handler)
        assert dispatcher.registry[UserCreatedEvent] == [handler]

    def test_second_subscriber_appends_to_the_same_list(self, dispatcher):
        async def handler_a(event):
            pass

        async def handler_b(event):
            pass

        dispatcher.subscribe(UserCreatedEvent, handler_a)
        dispatcher.subscribe(UserCreatedEvent, handler_b)
        assert dispatcher.registry[UserCreatedEvent] == [handler_a, handler_b]

    def test_different_event_types_get_separate_lists(self, dispatcher):
        async def handler(event):
            pass

        class OtherEvent(Event):
            pass

        dispatcher.subscribe(UserCreatedEvent, handler)
        dispatcher.subscribe(OtherEvent, handler)
        assert dispatcher.registry[UserCreatedEvent] == [handler]
        assert dispatcher.registry[OtherEvent] == [handler]


class TestPublish:
    def test_calls_the_subscribed_handler_with_the_event(self, dispatcher):
        received = []

        async def handler(event):
            received.append(event)

        dispatcher.subscribe(UserCreatedEvent, handler)
        event = UserCreatedEvent(user_id=1)
        _publish_and_run(dispatcher, event)
        assert received == [event]

    def test_calls_every_handler_subscribed_to_the_event(self, dispatcher):
        received = []

        async def handler_a(event):
            received.append("a")

        async def handler_b(event):
            received.append("b")

        dispatcher.subscribe(UserCreatedEvent, handler_a)
        dispatcher.subscribe(UserCreatedEvent, handler_b)
        _publish_and_run(dispatcher, UserCreatedEvent(user_id=1))
        assert set(received) == {"a", "b"}

    def test_ignores_handlers_subscribed_to_a_different_event_type(self, dispatcher):
        received = []

        async def handler(event):
            received.append(event)

        class OtherEvent(Event):
            pass

        dispatcher.subscribe(UserCreatedEvent, handler)
        _publish_and_run(dispatcher, OtherEvent())
        assert received == []

    def test_does_nothing_when_there_are_no_subscribers(self, dispatcher):
        dispatcher.publish(UserCreatedEvent(user_id=1))

    def test_does_not_wait_for_the_handler_to_complete(self, dispatcher):
        finished = []

        async def slow_handler(event):
            await asyncio.sleep(0.05)
            finished.append(True)

        dispatcher.subscribe(UserCreatedEvent, slow_handler)

        async def run():
            dispatcher.publish(UserCreatedEvent(user_id=1))
            assert finished == []
            await asyncio.sleep(0.1)
            assert finished == [True]

        asyncio.run(run())

    def test_a_raising_handler_does_not_propagate_to_the_caller(self, dispatcher):
        async def bad_handler(event):
            raise ValueError("boom")

        dispatcher.subscribe(UserCreatedEvent, bad_handler)
        _publish_and_run(dispatcher, UserCreatedEvent(user_id=1))

    def test_a_raising_handler_does_not_stop_other_handlers(self, dispatcher):
        received = []

        async def bad_handler(event):
            raise ValueError("boom")

        async def good_handler(event):
            received.append(event)

        dispatcher.subscribe(UserCreatedEvent, bad_handler)
        dispatcher.subscribe(UserCreatedEvent, good_handler)
        event = UserCreatedEvent(user_id=1)
        _publish_and_run(dispatcher, event)
        assert received == [event]

    def test_a_raising_handler_is_logged(self, dispatcher, capsys):
        async def bad_handler(event):
            raise ValueError("boom")

        dispatcher.subscribe(UserCreatedEvent, bad_handler)
        _publish_and_run(dispatcher, UserCreatedEvent(user_id=1))
        output = capsys.readouterr().out
        assert "bad_handler" in output
        assert "boom" in output
