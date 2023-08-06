import asyncio
from typing import AsyncGenerator


def __init__(hub):
    hub.beacon.local.QUEUE = asyncio.Queue()


STOP_ITERATION = object()


async def listen(hub) -> AsyncGenerator:
    """
    listen for data on the local queue
    """
    async for event in hub.beacon.local.channel():
        yield event


async def channel(hub) -> AsyncGenerator:
    while hub.beacon.RUN_FOREVER:
        event = await hub.beacon.local.QUEUE.get()
        if event is STOP_ITERATION:
            return
        yield event

    hub.log.debug("No more messages in local queue")


async def stop(hub):
    await hub.beacon.local.QUEUE.put(STOP_ITERATION)
