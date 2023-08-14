"""Run an example script to quickly test."""
import asyncio, pprint

from aiohttp import ClientSession

from pyiqvia import Client
from pyiqvia.errors import IQVIAError


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession):
    """Run."""
    try:
        client = Client("98230",websession)
        print(f"\n['{client.zip_code}']")
        print('\n---------------------------------\'Current\'----------------------------------')
        pprint.pprint(await client.allergens.current())
        print('-----------------------------------------------------------------------------')
        print('\n\n---------------------------------\'Extended\'----------------------------------')
        pprint.pprint(await client.allergens.extended())
        print('-----------------------------------------------------------------------------')
        print('\n\n---------------------------------\'Historic\'----------------------------------')
        pprint.pprint(await client.allergens.historic())
        print('----------------------------------------------------------------------------')
        print('\n\n---------------------------------\'Outlook\'----------------------------------')
        pprint.pprint(await client.allergens.outlook())
        print('----------------------------------------------------------------------------\n\n')

    except IQVIAError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
