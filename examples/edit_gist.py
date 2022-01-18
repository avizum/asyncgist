import asyncio

from aiohttp import ClientSession
from asyncgist import Client, File


async def main():
    client = Client("token", ClientSession())
    gist = await client.update(
        id_or_url="gist_url_or_id_here",
        description="New gist description",
        files=[
            File(
                filename="file.txt",
                content="edited files word word"
            ),
            File(
                filename="file.py",
                content="print('Goodbye, world.')"
            )
        ]
    )
    print(gist.html_url)
    await client.close()

asyncio.run(main())
