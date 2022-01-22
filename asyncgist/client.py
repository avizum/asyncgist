import aiohttp
import re

from typing import List, Union
from .models import Gist, File, Comment
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
        :class:`HTTPException`

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

    async def post_gist(self, *, description: str, files: Union[File, List[File]], public: bool) -> Gist:
        """
        Posts a Gist.

        Parameters
        ----------
        description: :class:`str`
            The description of the Gist.
        files: Union[:class:`File`, List[:class:`File`]]
            One or list of :class:`File` is required.
        public: :class:`bool`
            Indicate whether the Gist is public.
        raw: :class:`bool`
            Whether to return raw json or the url of the Gist.

        Returns
        -------
        :class:`Gist`
            The Gist that was created.
        """
        if not isinstance(files, list):
            files = [files]
        files = {f.filename: {"content": f.content} for f in files}

        data = {"public": public, "files": files, "description": description}
        output = await self.request(Request("POST"), json=data)
        return Gist(self, output)

    async def update_gist(self, *, id_or_url: str, description: str, files: Union[File, List[File]]) -> Gist:
        """
        Updates a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or the url of the Gist that you want to update.
        description: Optional[:class:`str`]
            The new description of the Gist.
        files: Union[:class:`File`, List[:class:`File`]]
            The new files or files to be updated.

        Raises
        ------
        :class:`NotFound`
            The Gist could not be found.

        Returns
        -------
        :class:`Gist`
            The newly updated Gist.
        """
        gist_id = convert(id_or_url)
        if not isinstance(files, list):
            files = [files]
        files = {f.filename: {"content": f.content} for f in files}
        data = {"description": description, files: files}
        output = await self.request(Request("PATCH", f"/{gist_id}"), json=data)
        return Gist(self, output)

    async def fetch_gist(self, id_or_url: str) -> Gist:
        """
        Fetches a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url for the Gist.

        Raises
        ------
        :class:`NotFound`
            The Gist is not found.
        :class:`Forbidden`
            You do not have permission to see this Gist.

        Returns
        -------
        :class:`Gist`
        """
        gist_id = convert(id_or_url)
        output = await self.request(Request("GET", f"/{gist_id}"))
        return Gist(self, output)

    async def delete_gist(self, id_or_url: str) -> None:
        """
        Deletes a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist you want to delete.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("DELETE", f"/{gist_id}"))

    async def star_gist(self, id_or_url: str) -> None:
        """
        Stars a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist you want to star.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("PUT", f"/{gist_id}/star"))

    async def unstar_gist(self, id_or_url: str) -> None:
        """
        Stars a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id of the Gist you want to unstar.
        """
        gist_id = convert(id_or_url)
        return await self.request(Request("DELETE", f"/{gist_id}/star"))

    # async def check_star(self, gist_id: str):
    #     """
    #     Checks whether a Gist is starred.
    #     """
    #     await self.session.request("GET", f"{self.url}/{gist_id}/star")

    async def fork_gist(self, id_or_url: str) -> Gist:
        """
        Fork a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist that you want to fork.

        Raises
        ------
        :class:`NotFound`
            The Gist was not found.
        :class:`Forbidden`
            You do not have permission to fork or see the Gist.

        Returns
        -------
        :class:`Gist`
            The Gist that was forked.
        """
        gist_id = convert(id_or_url)
        output = await self.request(Request("POST", f"/{gist_id}/forks"))
        return Gist(self, output)

    async def fetch_comments(self, id_or_url: str, per_page: int = 30, page: int = 1) -> List[Comment]:
        """
        Fetches comments of a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist that you want to fetch comments from.
        per_page: :class:`int`
            How many results per page. (Default: `30`, Maximum: `100`)
        page: :class:`int`
            Page number of the results to fetch. (Default: `1`)

        Raises
        ------
        :class:`NotFound`
            The Gist was not found.
        :class:`Forbidden`
            You do not have permission to fetch the Gist's comments or see the Gist.

        Returns
        -------
        List[:class:`Comment`]
            The list of comments.
        """
        gist_id = convert(id_or_url)
        data = {"per_page": per_page, "page": page}
        output = await self.request(Request("GET", f"/{gist_id}/comments"), data)
        return [Comment(comment) for comment in output]

    async def post_comment(self, id_or_url: str, content: str) -> Comment:
        """
        Posts a comment on a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist that you want to post a comment on.
        content: :class:`str`
            The content of the comment.

        Raises
        ------
        :class:`NotFound`
            The Gist was not found.
        :class:`Forbidden`
            You do not have permission to post comments or see the Gist.

        Returns
        -------
        :class:`Comment`
            The posted comment.
        """
        gist_id = convert(id_or_url)
        data = {"content": content}
        output = await self.request(Request("GET", f"/{gist_id}/comments"), data)
        return Comment(output)

    async def update_comment(self, id_or_url: str, comment_id: int, content: str) -> Comment:
        """
        Updates a comment in a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist.
        comment_id: :class:`int`
            The id of the comment.

        Raises
        ------
        :class:`NotFound`
            The Gist or comment was not found.
        :class:`Forbidden`
            You do not have permission to edit the comment, or view the Gist.

        Returns
        -------
        :class:`Comment`
            The edited comment.
        """
        gist_id = convert(id_or_url)
        data = {"body": content}
        output = await self.request(Request("PATCH", f"/{gist_id}/comments/{comment_id}"), data)
        return Comment(output)

    async def delete_comment(self, id_or_url: str, comment_id: int) -> None:
        """
        Updates a comment in a Gist.

        Parameters
        ----------
        id_or_url: :class:`str`
            The id or url of the Gist.
        comment_id: :class:`int`
            The id of the comment.

        Raises
        ------
        :class:`NotFound`
            The Gist or comment was not found.
        :class:`Forbidden`
            You do not have permission to delete the comment, or view the Gist.

        """
        gist_id = convert(id-id_or_url)
        return await self.request(Request("DELETE", f"/{gist_id}/comments/{comment_id}"))

    async def close(self):
        if not self.session.closed:
            await self.session.close()
