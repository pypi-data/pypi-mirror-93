# Python Client

## Installation

\$ pip install mona-client

## Environment variables

Mona uses several environment variables you need to set in order for things to
work as intended:

MONA_HOST - the Mona server's IP address you get from Mona.
MONA_PORT - The port for the above address.
MONA_USER_ID - A unique user id we provide for you.

## Quick Start and Example

- Install as mentioned above
- Set environment variables as mentioned above
- Instrument code with client as seen below

```
from mona_client import client

# Only call once,
# Add parameteres (host, port, ...) on this call if not already set through env vars.
client.init_client()

...

# In this example, iterating over data from a pre-existing DB.
# However, in other cases you might send out the data from any place within your system.
for context_instance in my_data:
    # Each context_instance contains a "row" data that we'd like to export to Mona.
    #
    # The arc_class arg must exist and will contain the name of the context class, which
    # should correspond to the context class in your confiuration file (corresponds to
    # the Mona data table this information will be saved in. see docs.monalabs.io for
    # more details).
    #
    # The context_id is a unique identifier for the current context instance
    # (corresponds to a row in Mona's processed database). This id can be used to update
    # context instances asynchronously. If none is given, Mona will create a random uuid
    # for it. This is highly unrecomended - since it takes away the option to update
    # this data in the future.
    #
    # The export_timestamp should contain a timestamp (seconds since epoch) for this
    # context instance (defaults to current time). This is useful for anytime you're
    # exporting data not in real time (e.g., backfilling, backtesting, or even simple
    # daily batch jobs).
    with client.new_mona_context(arc_class="MY_COOL_ALGORITHM_NAME",
                                 context_id=context_instance.unique_id,
                                 export_timestamp=context_instance.timestamp_seconds):
        ...
        # In this example, context_instance.relevant_monitoring_information contains a
        # dict with all the data needed for monitoring. This dict must be json
        # serializable. You can call "export" several times per context instance.
        # The data will be aggregated on Mona's server.
        client.export(context_instance.relevant_monitoring_information,
                      export_timestamp=context_instance.timestamp_seconds)
        ...
```

## Special field names

Don't use field names with "MONA\_" as their prefix. Mona uses this pattern
internally. If you do that, these fields will be discarded before being emitted
to Mona.

## Concurrency

Mona saves the ARC's id as a special variable, which is local to the thread and
to greenlets. This means that if you start a new thread/greenlet, by default the
new thread will have an empty context.

This is usually the preffered behavior, as a new thread usually means a new
received request (on servers) or a completely new run of an algorithm.

If by any chance you'd like to continue with the same context on a new thread,
just use the child class MonaThread under mona_thread.py. This class takes
care of transferring the full context id to the newly started thread.

```
from mona_client import client
from mona_client.mona_thread import MonaThread

def threaded_function():
    print(client.get_full_context_id() == main_context)

with client.new_mona_context(arc_class="threaded_algorithm_name"):
    global main_context
    main_context = client.get_full_context_id()
    MonaThread(target=threaded_function).start()  # Prints "True"
```

## Configuration and Big Red Button

If you'd like to set up configuration for mona, you can fill a simple json
configuration file. See mona_client_config.json for the default configuration
file used. There is currently only one configuration option, which is the "Big
Red Button" - the "disable_all" configuration, which, when set to true,
completely disables all mona activity (no more exporting and context inits).

Mona listens to changes on the configuartion file under the environment variable
"MONA_CLIENT_CONFIG_FILE". So if you want to disable mona while running, just
change "disable_all" from "false" to "true" in your config file and mona will
update automatically.

If you don't set MONA_CLIENT_CONFIG_FILE yourself, Mona will use a default
configuration file located on mona_client/config/mona_client_config.json. If
logging is enabled, Mona will log out the full address of this file on startup.
You can then make changes to that file to update configuration while mona is
running.

Another option to quickly disable all Mona activity, is to set the
MONA_DISABLE_ALL environment variable to a truthy value.

## Logging

Mona is using it's own logger named "mona-logger". You can configure it in your
code by just calling
'''
logging.getLogger("mona-logger")
'''
and then setting handlers and formatters as you please.

You can also configure Mona's logging using two different environment
variables:

1. MONA_LOGGING_LEVEL - set this to a level according to python's logging
   constants (e.g., 10 = debug)
2. MONA_PRINT_LOGS - set this to true if you want Mona to print logs to stdout.

## Testing the client code

The client's tests are written using the pytest framework, so in order to run
the tests (assuming you have pytest and pytest-mock installed on your environment), you just
need to type "pytest" to your shell.

## Uploading new version to PyPI

The main reference to follow to do that is on:
https://packaging.python.org/tutorials/packaging-projects/

- Register on PyPI with your mona email: https://pypi.org/
- Ask itai@monalabs.io to add you as collaborator
- If not installed, install twine: \$ python3 -m pip install --user --upgrade twine
- Change version number under setup.py
- If a new dependency is required, add it under setup.py under "install_requires"
- If not installed, install build tools: \$ python3 -m pip install --user --upgrade setuptools wheel
- Build new version: \$ python3 setup.py sdist bdist_wheel
- Upload new version (can change '\*' to actual version): \$ python -m twine upload dist/\*
