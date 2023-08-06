import asyncio
from typing import AsyncGenerator, Any, Dict, List

STOP_ITERATION = object()


def __init__(hub):
    hub.beacon.STARTED = False
    hub.beacon.RUN_FOREVER = True
    hub.pop.sub.add(dyne_name="evbus")
    hub.pop.sub.load_subdirs(hub.beacon)


def cli(hub):
    """
    Start up on the cli and print out the returns as they come
    """
    hub.pop.config.load(["beacon", "evbus", "acct", "rend"], cli="beacon")
    hub.pop.loop.create()

    beacon_profiles = hub.pop.Loop.run_until_complete(
        hub.evbus.init.profiles(
            subs=["beacon"],
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            acct_profiles=hub.OPT.evbus.ingress_profiles,
        )
    )
    evbus_profiles = hub.pop.Loop.run_until_complete(
        hub.evbus.init.profiles(
            subs=["evbus"],
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            acct_profiles=hub.OPT.evbus.ingress_profiles,
        )
    )
    coros = [
        hub.pop.Loop.create_task(
            hub.beacon.init.start(
                format_plugin=hub.OPT.beacon.format, sub_profiles=beacon_profiles
            )
        ),
        hub.pop.Loop.create_task(hub.evbus.init.start(evbus_profiles)),
        hub.evbus.init.print(renderer=hub.OPT.rend.output),
    ]
    if hub.OPT.evbus.random:
        coros.append(hub.evbus.test.start())

    try:
        for task in asyncio.as_completed(coros, loop=hub.pop.Loop):
            hub.pop.Loop.run_until_complete(task)
    except KeyboardInterrupt:
        hub.log.debug("Shutting down beacons")


async def start(hub, format_plugin: str, sub_profiles: Dict[str, Dict[str, Any]]):
    """
    Listen to all the beacon plugins, process events as they come in and vomit processed events to egress plugins
    """
    listeners_ = hub.beacon.init.listeners(sub_profiles)
    generator = hub.pop.loop.as_yielded(listeners_)

    # Ready to start a loop of generators
    hub.beacon.STARTED = True
    await asyncio.sleep(0)

    async for event, ref in generator:
        if event is STOP_ITERATION:
            hub.log.debug("Iterator was forced to stop")
            return

        processed = hub.beacon.format[format_plugin].apply(event, ref)
        await hub.evbus.BUS.put(processed)


async def join(hub):
    """
    Block until the event bus and beacons are started
    """
    await hub.evbus.init.join()

    while not hub.beacon.STARTED:
        await asyncio.sleep(0)


async def stop(hub):
    hub.log.debug("Shutting down beacons")
    # Stop beacons
    hub.beacon.RUN_FOREVER = False
    hub.evbus.RUN_FOREVER = False
    await hub.beacon.local.stop()
    await hub.evbus.init.stop()


def listeners(hub, contexts: Dict[str, Any]) -> List[AsyncGenerator]:
    ret = []

    hub.log.debug("Starting beacon listeners")
    for plugin in hub.beacon:
        name = plugin.__name__
        # If the listen function of a beacon has ctx, then populate it from acct
        if "ctx" in plugin.listen.signature.parameters:
            # Iterate over the defined profiles for the plugin
            for profile, ctx in contexts.get(name, {}).items():
                # Inject the ctx from the profile into the listener
                hub.log.debug(f"Created {name} beacon with ctx")
                ret.append(plugin.listen(ctx))
        else:
            hub.log.debug(f"Created {name} beacon")
            ret.append(plugin.listen())

    return ret


async def listen(hub) -> AsyncGenerator:
    """
    Listen for the stop signal then break out and shutdown everything
    """
    while hub.beacon.RUN_FOREVER:
        await asyncio.sleep(1)
    yield STOP_ITERATION
