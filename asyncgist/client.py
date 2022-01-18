import aiohttp
import re

from typing import List, Union
from .models import Gist, File
from .exceptions import NotFound, Forbidden, HTTPExeption

GIST_URL = "https://api.github.com/gists"
URL_REGEX = re.compile(r"https?://(?:www\.)?.+")


def convert(id_or_url: str) -> str:
    return id_or_url.split("/")[-1] if URL_REGEX.match(id_or_url) else id_or_url


class Request:
    def __init__(self, method: str, path: str = ""):
        self.method = method
        self.path = path
        self.url = f"{GIST_URL}{path}"


class Client:
    """
    Gist client that uses the GitHub Rest API.

    Parameters
    ----------
    token: :class:`str`
        The GitHub authorization token.
    session: :class:`aiohttp.ClientSession`
        The session used to connect to the API.
    """

    def __init__(self, token: str, session: aiohttp.ClientSession) -> None:
        self.token = token
        self.session = session

        self.session.headers["Accept"] = "application/vnd.github.v3+json"
        self.session.headers["User-Agent"] = "Avimetry-Gist-Cog"
        self.session.headers["Authorization"] = f"token {self.token}"

    async def request(self, request: Request, **kwargs) -> dict:
        """
        Handles requests.

        Parameters
        ----------
        request: :class:`Request`
        **kwargs: :class:`dict`

        Raises
        ------
        :class:`NotFound`
        :class:`Forbidden`
        :class: `HTTPException`

        Returns
        -------
        :class:`dict`
            The raw json response.
        """
        resp = await self.session.request(request.method, request.url, **kwargs)
        if 300 > resp.status >= 200:
            try:
                item = await resp.json()
            except Exception:
                item = None
            return item
        elif resp.status == 404:
            raise NotFound(resp.status, resp.reason, await resp.text())
        elif resp.status == 403:
            raise Forbidden(resp.status, resp.reason, await resp.text())
        else:
            raise HTTPExeption(resp.status, resp.reason, await resp.text())

    async def post(self, *, description: str, files: Union[File, List[File]], public: bool) -> Gist:
        """
        Posts a gist.

        Parameters
        ----------
        description: :class:`str`
            The description of the gist.
        files: Union[:class:`File`, List[:class:`File`]]
            One or list of :class:`File` is required.
        public: :class:`bool`
            Indicate whether the gist is public.
        raw: :class:`bool`
            Whether to return raw json or the url of the gist.

        Returns
        -------
        :class:`Gist`
            The gist that was created.
        """
        if not isinstance(files, list):
            files = [files]
        files = {f.filename: {"content": f.content} for f in files}

        data = {"public": public, "files": files, "description": description}
        output = await self.request(Request("POST"), json=data)
        return Gist(output)

    async def update(self, *, id_or_url: str, description: str, files: Union[File, List[File]]) -> Gist:
        """
        Updates a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or the url of the gist that you want to update.
        description: Optional[:class:`str`]
            The new description of the gist.
        files: Union[:class:`File`, List[:class:`File`]]
            The new files or files to be updated.

        Returns
        -------
        :class:`Gist`
            The newly updated gist.
        """
        gist_id = convert(id_or_url)
        if not isinstance(files, list):
            files = [files]
        files = {f.filename: {"content": f.content} for f in files}
        data = {"description": description, files: files}
        output = await self.request(Request("PATCH", f"/{gist_id}"), json=data)
        return Gist(output)

    async def get(self, id_or_url: str) -> Gist:
        """
        Gets a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url for the gist.

        Raises
        ------
        :class:`NotFound`
            The gist is not found.
        :class:`Forbidden`
            You do not have permission to see this gist.

        Returns
        -------
        :class:`Gist`
        """
        gist_id = convert(id_or_url)
        print(gist_id)
        output = await self.request(Request("GET", f"/{gist_id}"))
        return Gist(output)

    async def delete(self, id_or_url: str) -> None:
        """
        Deletes a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the gist you want to delete.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("DELETE", f"/{gist_id}"))

    async def star(self, id_or_url: str) -> None:
        """
        Stars a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the gist you want to star.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("PUT", f"/{gist_id}/star"))

    async def unstar(self, id_or_url: str) -> None:
        """
        Stars a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id of the gist you want to unstar.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("DELETE", f"/{gist_id}/star"))

    # async def check_star(self, gist_id: str):
    #     """
    #     Checks whether a gist is starred.
    #     """
    #     await self.session.request("GET", f"{self.url}/{gist_id}/star")

    async def fork(self, id_or_url: str) -> Gist:
        """
        Fork a gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the gist that you want to fork.

        Raises
        ------
        :class:`NotFound`
            The gist was not found.
        :class:`Forbidden`
            You do not have permission to fork or see the gist.

        Returns
        -------
        :class:`Gist`
            The gist that was forked.
        """
        gist_id = convert(id_or_url)
        output = await self.request(Request("POST", f"/{gist_id}/forks"))
        return Gist(output)

    async def close(self):
        if not self.session.closed:
            await self.session.close()
