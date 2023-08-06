# https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/1-introduction.html
from typing import AsyncGenerator


def __virtual__(hub):
    return hub.acct.beacon.pika.HAS_LIBS


async def listen(hub, ctx) -> AsyncGenerator:
    if not ctx.connected:
        hub.log.warning("No server to listen on for pika plugin")
        return

    listeners = [hub.beacon.pika.channel(ctx, ch) for ch in ctx.channels]
    generator = hub.pop.loop.as_yielded(listeners)

    async for message in generator:
        async with message.process():
            yield message.body.decode()

    hub.log.debug("No more messages in ampq queue")


async def channel(hub, ctx, name: str) -> AsyncGenerator:
    c = await ctx.connection.channel()
    queue = await c.declare_queue(name)
    hub.log.debug(f"Connected to amqp server channel {name}")

    async with queue.iterator() as q_iter:
        hub.log.debug(f"Started ampq iterator on channel {name}")
        async for message in q_iter:
            yield message

    hub.log.debug("No more messages in ampq queue")
