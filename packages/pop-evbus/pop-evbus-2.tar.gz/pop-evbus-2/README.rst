=====
EVBUS
=====

An asynchronous message ingress system.
Messages that are put onto the event bus are "vomited" to all the ingress plugin publishers.

INSTALLATION
============

.. code-block:: bash

    pip install pop-evbus

USAGE
=====

`evbus` is mainly an app-merge component for larger projects.
However, it includes a script that can be useful for testing your ingress queues.
This testing script can randomly generate data and put it on the event bus -- which gets propagated to the ingress publishers.
A listener iterates over the internal ingress queue and prints everything that gets posted to it.
The the outputter to format the printed data can be specified with `--output`.
The `--random` flag starts a coroutine that periodically populates the event bus with random data.

.. code-block:: bash

    evbus_test --output json --random

TESTING
=======

Install `evbus` locally with testing libraries:

.. code-block:: bash

    $ git clone git@gitlab.com:saltstack/pop/evbus.git
    $ pip install -e evbus -r requirements-test.txt

If you have a rabbitmq-server binary installed via your system's package manager, the pika tests won't be skipped.
Start a local rabbitmq-server with the default parameters:

.. code-block:: bash

    sudo rabbitmq-server

Run the tests with pytest:

.. code-block:: bash

    $ pytest evbus/tests


ACCT PROFILES
=============

`evbus` will read credentials that are encrypted using the `acct` system.
To use this system, create a yaml file that has the plaintext credentials and information needed
to connect with the various ingress plugins.
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
        ingress_channels:
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

    $ export ACCT_FILE=$PWD/credentials.yml.fernet
    $ export ACCT_KEY="YeckEnWEGOjBDVxxytw13AsdLgquzhCtFHOs7kDsna8="

They can also be used on the command line:

.. code-block:: bash

    $ evbus_test --acct-file=credentials.yml.fernet --acct-key="YeckEnWEGOjBDVxxytw13AsdLgquzhCtFHOs7kDsna8="


INTEGRATION
===========

Your own app can extend `acct`'s command line interface to use the `--acct-file` and `--acct-key` options for evbus:

my_project/conf.py

.. code-block:: python

    CLI_CONFIG = {
        "acct_file": {"source": "acct", "os": "ACCT_FILE"},
        "acct_key": {"source": "acct", "os": "ACCT_KEY"},
        "ingress_profiles": {"source": "evbus"},
    }


In your own project, you can vertically merge `evbus` and extend it with your own ingress plugins:

my_project/conf.py

.. code-block:: python

    DYNE = {
        "acct": ["acct"],
        "evbus": ["evbus"],
        "my_project": ["my_project"],
    }

Create the directory `my_project/ingress` and add your ingress plugins there.

ingress plugins need a function called "publish" that takes a parameter called "event"

my_project/ingress/my_plugin.py

.. code-block:: python

    async def publish(hub, event):
        await my_queue.put(event)

The "publish" function can optionally have a `ctx` parameter if your ingress plugin requires login credentials.
The `ctx` parameter will be automatically be populated by `acct`  and `evbus` if a profile that specifies your
plugin is included in the encrypted acct file.

my_project/ingress/my_plugin.py

.. code-block:: python

    async def publish(hub, ctx, event):
        for channel in ctx.channels:
            probably_an_exchange_object = await ctx.connection.some_func(channel)
            await probably_an_exchange_object.publish_function(event)

Create the directory  `my_project/acct/evbus` and add your acct plugins there.
`acct` plugins need to implement a `gather` function, which reads the appropriate information from
`hub.acct.PROFILES` and turns it into processed profile information in `hub.acct.SUB_PROFILES`.
This processing can include operations such as opening a connection to a remote server.

my_project/acct/evbus/my_plugin.py

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
                    ingress_channels:
                      - channel1
                      - channel2
            """
            sub_profiles = {}
            for profile, ctx in hub.acct.PROFILES.get("my_plugin", {}).items():
                # Create a connection through [some_library] for each of the profiles
                sub_profiles[profile] = {
                    "connected": False,
                    "connection": await some_library.connect(**ctx),
                    "channels": ctx.pop("ingress_channels", []),
                }
            # Return these to be automatically processed by acct and injected into the `ctx` parameter of appropriate ingress publish calls.
            return sub_profiles


Add evbus startup code to your project's initializer:

my_project/my_project/init.py

.. code-block:: python

    def __init__(hub):
        # Horizontally merge the evbus dynamic namespace into your project
        hub.pop.sub.add(dyne_name="evbus")

    def cli(hub):
        # Load the config from evbus onto hub.OPT
        hub.pop.config.load(["my_project", "evbus", "acct"], cli="my_project")

        # Create the asyncio loop
        hub.pop.loop.create()

        # Create the event bus coroutine
        coro = hub.evbus.init.start(
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            ingress_profiles=hub.OPT.evbus.ingress_profiles,
        )

        # Start the event bus
        hub.pop.Loop.run_until_complete(coro)
