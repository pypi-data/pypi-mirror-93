# https://github.com/MagicStack/asyncpg

try:
    import asyncpg

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


async def gather(hub, profiles):
    """
    Get profile names from encrypted amqp credential files

    Example:
    .. code-block:: yaml

        pg:
          profile_name:
            host: localhost
            port: 5432
            user: user
            password: password
            database: database
            beacon_channels:
              - channel1
              - channel1
    """
    sub_profiles = {}
    for profile, ctx, in profiles.get("pg", {}).items():
        sub_profiles[profile] = {
            "connected": False,
            "channels": ctx.pop("beacon_channels", []),
            "connection": None,
        }

        hub.log.debug("connecting to PostgreSQL server")
        try:
            sub_profiles[profile]["connection"] = await asyncpg.connect(
                loop=hub.pop.Loop, **ctx
            )
            sub_profiles[profile]["connected"] = True
            hub.log.debug("connected to rabbitmq server")
        except Exception as err:
            hub.log.error("Could not connect to PostgreSQL server")
            hub.log.error(str(err))

    return sub_profiles
