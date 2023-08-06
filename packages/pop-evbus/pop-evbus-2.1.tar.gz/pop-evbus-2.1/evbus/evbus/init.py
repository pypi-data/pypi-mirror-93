import asyncio
from typing import List, Any, Dict
from dict_tools.data import NamespaceDict

__func_alias__ = {"print_": "print"}


STOP_ITERATION = object()


def __init__(hub):
    hub.evbus.STARTED = False
    hub.evbus.RUN_FOREVER = True
    hub.evbus.BUS = asyncio.Queue()
    for dyne in ("acct", "ingress", "output"):
        hub.pop.sub.add(dyne_name=dyne)


def cli(hub):
    hub.pop.config.load(["evbus", "acct", "rend"], cli="evbus")
    hub.pop.loop.create()

    sub_profiles = hub.pop.Loop.run_until_complete(
        hub.evbus.init.profiles(
            subs=["evbus"],
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            acct_profiles=hub.OPT.evbus.ingress_profiles,
        )
    )

    coros = [
        hub.evbus.init.start(sub_profiles=sub_profiles.get("evbus", {})),
        hub.evbus.init.print(renderer=hub.OPT.rend.output),
    ]

    if hub.OPT.evbus.random:
        coros.append(hub.evbus.test.start())

    try:
        for task in asyncio.as_completed(coros, loop=hub.pop.Loop):
            hub.pop.Loop.run_until_complete(task)
    except KeyboardInterrupt:
        hub.log.debug("Shutting down Event Bus")


async def start(hub, sub_profiles: Dict[str, Dict[str, Any]]):
    hub.log.debug("Starting event bus")
    publishers = await hub.ingress.init.publishers(sub_profiles)
    hub.evbus.STARTED = True

    while hub.evbus.RUN_FOREVER:
        # Block until another event is added to the queue
        await hub.evbus.BUS.join()
        event = await hub.evbus.BUS.get()
        if event is STOP_ITERATION:
            hub.log.debug("Event bus was forced to stop")
            return
        await hub.ingress.init.vomit(event, publishers)
        hub.evbus.BUS.task_done()


async def stop(hub):
    """
    Stop the event bus
    """
    hub.log.debug("Stopping the event bus")
    await hub.evbus.BUS.put(STOP_ITERATION)
    hub.evbus.RUN_FOREVER = False


async def join(hub):
    while not hub.evbus.STARTED:
        await asyncio.sleep(0, loop=hub.pop.Loop)


async def print_(hub, renderer: str = "json"):
    """
    Just print out the queue forever
    """
    hub.log.debug("Started evbus print loop")
    while hub.evbus.RUN_FOREVER:
        await asyncio.sleep(0)
        event = await hub.ingress.QUEUE.get()
        if event is hub.ingress.init.STOP_ITERATION:
            return

        print(hub.output[renderer].display(event))
        print("-" * 80)


async def profiles(
    hub,
    subs: List[str],
    acct_file: str = None,
    acct_key: str = None,
    acct_profiles: List[str] = None,
) -> Dict[str, Any]:
    """
    Read the acct information from the named subs and return the context
    """
    if acct_file and acct_key:
        hub.log.debug("Reading profiles from acct")
        all_profiles = await hub.acct.init.profiles(acct_file, acct_key)
    else:
        all_profiles = {}

    ret_profiles = NamespaceDict()

    # If acct_profiles is empty then use all profiles
    if acct_profiles:
        for provider, profile in all_profiles.items():
            ret_profiles[provider] = {}
            for name, info in profile.items():
                # Remove profiles that aren't specified in the acct_profiles
                if name in acct_profiles:
                    ret_profiles[provider][name] = info

    # Create sub profiles
    new_profiles = await hub.acct.init.process(subs, ret_profiles)

    sub_profiles = {}
    for sub in subs:
        sub_profiles.update(new_profiles.get(sub, {}))

    return sub_profiles
