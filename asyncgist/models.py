from __future__ import annotations
from datetime import datetime
from typing import List, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from .client import Client


class File:
    """
    Represents a Gist file.

    Attributes
    ----------
    filename: :class:`str`
        The name of the file.
    type: :class:`str`
        The file type.
    content: :class:`str`
        The file's content.
    language: :class:`str`
        The language that is used in the file.
    raw_url: :class:`str`
        The gist.githubusercontent.com url to the file.
    size: :class:`int`
        The size of the file.
    """
    def __init__(
        self,
        *,
        filename: str,
        type: str = None,
        content: str,
        language: str = None,
        raw_url: str = None,
        size: int = None
    ) -> None:
        self.filename = filename
        self.type = type
        self.content = content
        self.language = language
        self.raw_url = raw_url
        self.size = size

    def __repr__(self) -> None:
        return f"<File filename={self.filename} raw_url={self.raw_url} size={self.size}>"

    @classmethod
    def from_dict(cls, data: dict):
        self = cls.__new__(cls)
        self.filename = data.get("filename")
        self.type = data.get("type")
        self.content = data.get("content")
        self.language = data.get("language")
        self.raw_url = data.get("raw_url")
        self.size = data.get("size")
        return self


class User:
    """
    Represents a GitHub user.
    """
    def __init__(self, data: dict) -> None:
        self._set(data)

    def _set(self, data: dict) -> None:
        self.login: Union[str, None] = data.get("login")
        self.id: Union[int, None] = data.get("id")
        self.node_id: Union[str, None] = data.get("node_id")
        self.avatar_url: Union[str, None] = data.get("avatar_url")
        self.gravatar_id: Union[str, None] = data.get("gravatar_id")
        self.url: Union[str, None] = data.get("url")
        self.html_url: Union[str, None] = data.get("html_url")
        self.followers_url: Union[str, None] = data.get("followers_url")
        self.following_url: Union[str, None] = data.get("following_url")
        self.gists_url: Union[str, None] = data.get("gists_url")
        self.starred_url: Union[str, None] = data.get("starred_url")
        self.subscriptions_url: Union[str, None] = data.get("subscriptions_url")
        self.organizations_url: Union[str, None] = data.get("organizations_url")
        self.repos_url: Union[str, None] = data.get("repos_url")
        self.events_url: Union[str, None] = data.get("events_url")
        self.received_events_url: Union[str, None] = data.get("received_events_url")
        self.type: Union[str, None] = data.get("type")
        self.site_admin: Union[bool, None] = data.get("site_admin")


class Gist:
    """
    Represents a Gist.
    """
    def __init__(self, client: Client, data: dict) -> None:
        if not data.get("id"):
            raise ValueError("Gist must have an id.")
        self.client = client
        self._set(data)

    def __repr__(self) -> str:
        return f"<Gist html_url={self.html_url}>"

    def _set(self, data: dict) -> None:
        self.url: Union[str, None] = data.get("url")
        self.forks_url: Union[str, None] = data.get("forks_url")
        self.commits_url: Union[str, None] = data.get("commits_url")
        self.id: Union[int, None] = data.get("id")
        self.node_id: Union[str, None] = data.get("node_id")
        self.git_pull_url: Union[str, None] = data.get("git_pull_url")
        self.git_push_url: Union[str, None] = data.get("git_push_url")
        self.html_url: Union[str, None] = data.get("html_url")
        self.public: Union[bool, None] = data.get("public")
        self.description: Union[str, None] = data.get("description")
        self.comments: Union[dict, None] = data.get("comments")
        self.comments_url: Union[str, None] = data.get("comments_url")
        self.truncated: Union[bool, None] = data.get("truncated")

        created_at = data.get("created_at")
        created_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S%z")
        self.created_at: Union[datetime, None] = created_datetime

        updated_at = data.get("updated_at")
        updated_datetime = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S%z")
        self.updated_at: Union[datetime, None] = updated_datetime

        owner = data.get("owner")
        self.owner: Union[User, None] = owner if owner is None else User(owner)

        user = data.get("user")
        self.user: Union[User, None] = user if user is None else User(user)

        files = data.get("files")
        self.files: Union[List[File], None] = [File.from_dict(val) for _, val in files.items()]

    async def update(self, description: str, files: Union[File, List[File]]) -> Gist:
        """
        Updates the Gist.

        Parameters
        ----------
        description: Optional[:class:`str`]
            The new description of the Gist.
        files: Union[:class:`File`, List[:class:`File`]]
            The new files or files to be updated.

        Returns
        -------
        :class:`Gist`
            The newly updated Gist.
        """
        return await self.client.update_gist(id_or_url=self.id, description=description, files=files)

    async def delete(self) -> None:
        """
        Deletes the Gist.
        """
        return await self.client.delete_gist(self.id)

    async def star(self) -> None:
        """
        Stars the Gist.
        """
        return await self.client.star_gist(self.id)

    async def unstar(self) -> None:
        """
        Unstats the Gist.
        """
        return await self.client.unstar_gist(self.id)

    async def fork(self) -> Gist:
        """
        Forks the Gist.
        """
        return await self.client.fork_gist(self.id)

    async def post_comment(self, content: str):
        """
        Posts a comment on a Gist.

        Parameters
        ----------
        content: :class:`str`
            The content of the comment.

        Raises
        ------
        :class:`Forbidden`
            You do not have permission to post comments on the Gist.

        Returns
        -------
        :class:`Comment`
            The posted comment.
        """
        return await self.client.post_comment(self.id, content)

    async def fetch_comments(self, per_page: int = 30, page: int = 1) -> Union[Comment, List[Comment]]:
        """
        Fetches comments of a Gist.

        Parameters
        ----------
        per_page: :class:`int`
            How many results per page. (Default: `30`, Maximum: `100`)
        page: :class:`int`
            Page number of the results to fetch. (Default: `1`)

        Raises
        ------
        :class:`Forbidden`
            You do not have permission to fetch the Gist's comments.

        Returns
        -------
        List[:class:`Comment`]
            The list of comments.
        """
        return await self.client.fetch_comments(self.id, per_page, page)


class Comment:
    def __init__(self, data: dict):
        self._set(data)

    def _set(self, data: dict):
        self.id: Union[int, None] = data.get("id")
        self.node_id: Union[str, None] = data.get("node_id")
        self.url: Union[str, None] = data.get("url")
        self.body: Union[str, None] = data.get("body")

        user = data.get("user")
        self.user: User(user)
