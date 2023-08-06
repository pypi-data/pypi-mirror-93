import asyncio
import datetime
import random
from typing import AsyncGenerator


async def listen(hub) -> AsyncGenerator:
    i = 0
    hub.log.debug("started random data injector")
    while hub.evbus.RUN_FOREVER:
        randint = random.randint(0, 10000000)
        yield {
            "number": i,
            "timestamp": datetime.datetime.now().timestamp(),
            "data": f"{randint}".zfill(7),
        }
        i += 1
        await asyncio.sleep(1)


async def start(hub):
    async for event in hub.evbus.test.listen():
        await hub.evbus.BUS.put(event)
