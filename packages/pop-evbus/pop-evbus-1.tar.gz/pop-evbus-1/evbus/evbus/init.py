import asyncio
import copy
from typing import List, Any, Dict

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

    coros = []
    if hub.OPT.evbus.random:
        coros.append(hub.evbus.test.start())
    coros.extend(
        [
            hub.evbus.init.start(
                acct_file=hub.OPT.acct.acct_file,
                acct_key=hub.OPT.acct.acct_key,
                ingress_profiles=hub.OPT.evbus.ingress_profiles,
            ),
            hub.evbus.init.print(renderer=hub.OPT.rend.output),
        ]
    )

    try:
        for task in asyncio.as_completed(coros, loop=hub.pop.Loop):
            hub.pop.Loop.run_until_complete(task)
    except KeyboardInterrupt:
        hub.log.debug("Shutting down Event Bus")


async def start(
    hub, acct_file: str = None, acct_key: str = None, ingress_profiles: List[str] = None
):
    hub.log.debug("Starting event bus")
    sub_profiles = await hub.evbus.init.profiles(
        subs=["evbus"],
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profiles=ingress_profiles,
    )
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
    while hub.evbus.RUN_FOREVER:
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
    hub.log.debug("Reading profiles from acct")
    if acct_file and acct_key:
        hub.acct.init.unlock(acct_file, acct_key)

    all_profiles = copy.deepcopy(hub.acct.PROFILES)

    # If acct_profiles is empty then use all profiles
    if acct_profiles:
        for provider, profile in all_profiles.items():
            for name in profile:
                # Remove profiles that aren't specified in the acct_profiles
                if name not in acct_profiles:
                    hub.acct.PROFILES[provider].pop(name)
                    hub.log.debug(
                        f"Provider '{provider}' has a profile '{name}' not in the allowlist"
                    )

    # Create sub profiles
    await hub.acct.init.process_subs(subs)

    # Restore the original profiles
    hub.acct.PROFILES = all_profiles

    sub_profiles = {}
    for sub in subs:
        sub_profiles.update(hub.acct.SUB_PROFILES.get(sub, {}))

    return sub_profiles
