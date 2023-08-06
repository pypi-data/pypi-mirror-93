======
BEACON
======

A system to continually watch interfaces for events and forward them respectively through the event bus

INSTALLATION
============

.. code-block:: bash

    pip install pop-beacon

USAGE
=====

`beacon` is mainly an app-merge component for larger projects.
However, it includes a script that can be useful for testing your beacons.
This testing script will listen to all beacons and print out events that any of them receive.
A listener iterates over the internal beacon queues and prints everything that gets posted to them.
The the outputter to format the printed data can be specified with `--output`.

.. code-block:: bash

    beacon_test --output json

TESTING
=======

Install `beacon` locally with testing libraries:

.. code-block:: bash

    $ git clone git@gitlab.com:saltstack/pop/beacon.git
    $ pip install -e beacon -r requirements-test.txt

If you have a rabbitmq-server binary installed via your system's package manager, the pika tests won't be skipped.
Start a local rabbitmq-server with the default parameters:

.. code-block:: bash

    sudo rabbitmq-server

Run the tests with pytest:

.. code-block:: bash

    $ pytest beacon/tests


ACCT PROFILES
=============

`beacon` will read credentials that are encrypted using the `acct` system.
To use this system, create a yaml file that has the plaintext credentials and information needed
to connect with the various beacon plugins.
For example, to connect to a rabbitmq server, or any amqp implementation,
have a profile in your `acct` credentials file that specifies the "pika" acct plugin:

credentials.yml

.. code-block:: yaml

    pika:
      profile_name:
        host: localhost
        port: 5672
        username: XXXXXXXXXXXX
        password: XXXXXXXXXXXX
        beacon_channels:
          - channel1
          - channel2

Next use the `acct` command to encrypt this file using the fernet algorithm:

.. code-block:: bash

    $ acct credentials.yml
    New encrypted file created at: credentials.yml.fernet
    The file was encrypted with this key:
    YeckEnWEGOjBDVxxytw13AsdLgquzhCtFHOs7kDsna8=

The `acct` information can now be stored in environment variables:

.. code-block:: bash

    $ export ACCT_FILE = $PWD/credentials.yml.fernet
    $ export ACCT_KEY = "YeckEnWEGOjBDVxxytw13AsdLgquzhCtFHOs7kDsna8="

They can also be used on the command line:

.. code-block:: bash

    $ beacon_test --acct-file=credentials.yml.fernet --acct-key="YeckEnWEGOjBDVxxytw13AsdLgquzhCtFHOs7kDsna8="


INTEGRATION
===========

Your own app can extend `acct`'s command line interface to use the `--acct-file` and `--acct-key` options for beacon:

my_project/conf.py

.. code-block:: python

    CLI_CONFIG = {
        "acct_file": {"source": "acct", "os": "ACCT_FILE"},
        "acct_key": {"source": "acct", "os": "ACCT_KEY"},
        "beacon_profiles": {"source": "beacon"},
    }


In your own project, you can vertically merge `beacon` and extend it with your own beacon plugins:

my_project/conf.py

.. code-block:: python

    DYNE = {
        "acct": ["acct"],
        "beacon": ["beacon"],
        "my_project": ["my_project"],
    }

Create the directory `my_project/beacon` and add your beacon plugins there.

Beacon plugins need a function called "listen" that is an asynchronous generator.

my_project/beacon/my_plugin.py

.. code-block:: python

    from typing import AsyncGenerator

    async def listen(hub) -> AsyncGenerator:
        async for event in my_queue:
            yield event

The "listen" function can optionally have a `ctx` parameter if your beacon plugin requires login credentials.
The `ctx` parameter will be automatically be populated by `acct`  and `evbus` if a profile that specifies your
plugin is included in the encrypted acct file.

my_project/beacon/my_plugin.py

.. code-block:: python

    from typing import AsyncGenerator

    async def listen(hub, ctx) -> AsyncGenerator:
        if not ctx.connected:
            return

        # Many message queues have named channels that can be specified
        # Create a listener for every channel on this connection
        # A listener is another function that returns an async generator
        channel_listeners = [await ctx.connection.channel_listener(channel) for channel in ctx.channels]
        # Use hub.pop.loop.as_yielded to combine all the channel async generators into a single async generator
        generator = hub.pop.loop.as_yielded(channel_listeners)

        # Listen for events as they come from any of the channels
        async for event in generator:
            yield event

Create the directory  `my_project/acct/beacon` and add your acct plugins there.
`acct` plugins need to implement a `gather` function, which reads the appropriate information from
`hub.acct.PROFILES` and turns it into processed profile information in `hub.acct.SUB_PROFILES`.
This processing can include operations such as opening a connection to a remote server.

my_project/acct/beacon/my_plugin.py

.. code-block:: python

        async def gather(hub):
            """
            Get [my_plugin] profiles from an encrypted file

            Example:

            .. code-block:: yaml

                my_plugin:
                  profile_name:
                    host: localhost
                    port: 12345
                    username: XXXXXXXXXXXX
                    password: XXXXXXXXXXXX
                    beacon_channels:
                      - channel1
                      - channel2
            """
            sub_profiles = {}
            for profile, ctx in hub.acct.PROFILES.get("my_plugin", {}).items():
                # Create a connection through [some_library] for each of the profiles
                sub_profiles[profile] = {
                    "connected": False,
                    "connection": await some_library.connect(**ctx),
                    "channels": ctx.pop("beacon_channels", []),
                }
            # Return these to be automatically processed by acct and injected into the `ctx` parameter of appropriate beacon publish calls.
            return sub_profiles


Add beacon startup code to your project's initializer:

my_project/my_project/init.py

.. code-block:: python

    def __init__(hub):
        # Horizontally merge the beacon dynamic namespace into your project
        hub.pop.sub.add(dyne_name="beacon")

    def cli(hub):
        # Load the config from beacon onto hub.OPT
        hub.pop.config.load(["my_project", "beacon", "evbus", "acct"], cli="my_project")

        # Create the asyncio loop
        hub.pop.loop.create()

        # Create the beacon coroutine
        coro = hub.beacon.init.start(
            format_plugin=hub.OPT.beacon.format,
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            beacon_profiles=hub.OPT.beacon.beacon_profiles,
        )

        # Start the main beacon listener
        hub.pop.Loop.run_until_complete(coro)
