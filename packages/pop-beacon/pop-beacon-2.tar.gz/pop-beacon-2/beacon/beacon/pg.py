# https://github.com/MagicStack/asyncpg
import asyncio
from typing import AsyncGenerator

__func_alias__ = {"channel_": "channel"}


def __virtual__(hub):
    return hub.acct.beacon.pg.HAS_LIBS


async def listen(hub, ctx) -> AsyncGenerator:
    if not ctx.connected:
        hub.log.warning("No server to listen on for pika plugin")
        return

    # Send the message to end all channels for this context
    def _done(conn):
        hub.log.info("A PostgreSQL beacon has disconnected")
        ctx.connected = False

    ctx.connection.add_termination_listener(_done)
    ctx.connection.add_log_listener(hub.beacon.pg.log)

    listeners = [hub.beacon.pg.channel(ctx, channel) for channel in ctx.channels]
    generator = hub.pop.loop.as_yielded(listeners)

    async for message in generator:
        yield message

    hub.log.debug("No more messages in PostgreSQL queue")


async def channel_(hub, ctx, channel: str) -> AsyncGenerator:
    """
    Add a listener for the PostgreSQL channel.
    Route the callback to a local queue and turn this function into a generator fo the results
    """
    queue = asyncio.Queue()

    async def _callback(conn, pid, ch, payload):
        await queue.put(payload)

    await ctx.connection.add_listener(channel, _callback)

    while hub.beacon.RUN_FOREVER and ctx.connected:
        yield await queue.get()

    hub.log.debug(f"No more messages in PostgreSQL channel {channel}")


def log(hub, conn, message):
    """
    A log listener for pg queues
    """
    hub.log.debug(message)
