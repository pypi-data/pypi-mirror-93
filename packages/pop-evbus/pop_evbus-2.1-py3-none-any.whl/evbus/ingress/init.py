import asyncio
from typing import Dict, AsyncIterator, Any, List, Tuple

__func_alias__ = {"iter_": "iter", "publishers_": "publishers"}
STOP_ITERATION = object()


def __init__(hub):
    hub.ingress.RUN_FOREVER = True
    hub.ingress.QUEUE = asyncio.Queue()


async def publish(hub, event: Dict):
    await hub.ingress.QUEUE.put(event)


async def iter_(hub) -> AsyncIterator:
    """
    Iterate over the ingress queue until RUN_FOREVER is unset
    """
    while hub.ingress.RUN_FOREVER:
        event = await hub.ingress.QUEUE.get()
        if event is STOP_ITERATION:
            hub.log.debug("Cancelled iteration of ingress queue")
            return
        yield event


async def publishers_(
    hub, contexts: Dict[str, Any]
) -> List[Tuple["pop.contract.ContractedAsync", Dict[str, Any]]]:
    """
    For all the contexts and ingress plugins, find the
    """
    hub.log.debug("Collecting publisher plugins")
    ret = []

    for plugin in hub.ingress:
        name = plugin.__name__

        # If the listen function of ingress has ctx, then populate it from acct
        if "ctx" in plugin.publish.signature.parameters:
            # Iterate over the defined profiles for the plugin
            for profile, ctx in contexts.get(name, {}).items():
                # Inject the ctx from the profile into the listener
                hub.log.debug(f"Created {name} ingress with ctx")
                ret.append((plugin.publish, ctx))
        else:
            hub.log.debug(f"Created {name} ingress")
            ret.append((plugin.publish, None))

    return ret


async def vomit(
    hub,
    event: Dict,
    publishers: List[Tuple["pop.contract.ContractedAsync", Dict[str, Any]]],
):
    """
    Post an event to all the event queues
    """
    coros = []
    for publisher, ctx in publishers:
        if ctx is None:
            coros.append(publisher(event))
        else:
            coros.append(publisher(ctx, event))

    for coro in asyncio.as_completed(coros, loop=hub.pop.Loop):
        await coro
