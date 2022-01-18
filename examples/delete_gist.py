import asyncio

from aiohttp import ClientSession
from asyncgist import Client


async def main():
    client = Client("token", ClientSession())
    client.delete("gist_id_or_url_here")
    await client.close()

asyncio.run(main())
