import asyncio
from bleak import BleakScanner, discover


async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run())