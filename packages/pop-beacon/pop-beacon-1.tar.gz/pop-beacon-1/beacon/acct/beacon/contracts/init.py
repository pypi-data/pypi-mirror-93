from dict_tools import data
from typing import Any, Dict


async def post_gather(hub, ctx) -> Dict[str, Any]:
    return data.NamespaceDict(ctx.ret)


async def post_ctx(hub, ctx):
    return data.NamespaceDict(ctx.ret)
