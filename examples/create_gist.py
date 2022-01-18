import asyncio

from aiohttp import ClientSession
from asyncgist import Client, File


async def main():
    client = Client("token", ClientSession())
    gist = await client.post(
        description="Cool gist, right?",
        files=[
            File(
                filename="file.txt",
                content="This is a gist posted from asyncgist made by avizum."
            ),
            File(
                filename="file.py",
                content="print('Hello, world!')"
            )
        ],
        public=True
    )
    print(gist.html_url)
    await client.close()

asyncio.run(main())
