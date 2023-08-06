from typing import AsyncGenerator


async def sig_listen(hub, ctx) -> AsyncGenerator:
    ...


async def call_listen(hub, ctx):
    # Inject the ctx.ref into the yield results
    async for ret in ctx.func(*ctx.args, **ctx.kwargs):
        yield ret, ctx.ref
