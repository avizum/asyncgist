from __future__ import annotations
from datetime import datetime
from typing import List, Union, Optional, TYPE_CHECKING
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
        self.login: Optional[str] = data.get("login")
        self.id: Optional[int] = data.get("id")
        self.node_id: Optional[str] = data.get("node_id")
        self.avatar_url: Optional[str] = data.get("avatar_url")
        self.gravatar_id: Optional[str] = data.get("gravatar_id")
        self.url: Optional[str] = data.get("url")
        self.html_url: Optional[str] = data.get("html_url")
        self.followers_url: Optional[str] = data.get("followers_url")
        self.following_url: Optional[str] = data.get("following_url")
        self.gists_url: Optional[str] = data.get("gists_url")
        self.starred_url: Optional[str] = data.get("starred_url")
        self.subscriptions_url: Optional[str] = data.get("subscriptions_url")
        self.organizations_url: Optional[str] = data.get("organizations_url")
        self.repos_url: Optional[str] = data.get("repos_url")
        self.events_url: Optional[str] = data.get("events_url")
        self.received_events_url: Optional[str] = data.get("received_events_url")
        self.type: Optional[str] = data.get("type")
        self.site_admin: Optional[bool] = data.get("site_admin")


class Gist:
    """
    Represents a Gist.

    Attributes
    ----------
    url: Optional[:class:`str`]
        The api url of the Gist.
        To get the url leading to the Gist, use `html_url`
    forks_url: Optional[:class:`str`]
        The url for Gist forks.
    commits_url: Optional[:class:`str`]
        The url for the Gist's commits.
    id: Optional[:class:`int`]
        The id of this Gist.
    node_id: Optional[:class:`str`]
        The node id of this Gist.
    git_pull_url: Optional[:class:`str`]
        The pull url of this Gist.
    git_push_url: Optional[:class:`str`]
        The push url of this Gist.
    html_url: Optional[:class:`str`]
        The url leading to the Gist.
    public: [Optional:class:`bool`]
        Whether the Gist is public or secret
    description: Optional[:class:`str`]
        The description of the Gist.
    comments: List[:class:`Comment`]
        List of the Gist's comments.
    comments_url: Optional[:class:`str`]
        The url for the comments on the Gist.
    truncated: Optional[:class:`bool`]
        Whether the Gist is truncated.
    created_at: Optional[:class:`datetime`]
        datetime object for when the Gist was created.
    updated_at: opetional[:class:`datetime`]
        datetime object for when the Gist was last updated.
    owner: :Optional[class:`User`]
        The owner of the Gist.
    user: Optional[:class:`User`]
        The user of the Gist.
    files: Union[List[:class:`File`], :class:`File`]
        List of files the Gist contains.
    """
    def __init__(self, client: Client, data: dict) -> None:
        if not data.get("id"):
            raise TypeError("Gist data must have an id.")
        self.client: Client = client
        self._set(data)

    def __repr__(self) -> str:
        return f"<Gist html_url={self.html_url}>"

    def _set(self, data: dict) -> None:
        self.url: Optional[str] = data.get("url")
        self.forks_url: Optional[str] = data.get("forks_url")
        self.commits_url: Optional[str] = data.get("commits_url")
        self.id: Optional[int] = data.get("id")
        self.node_id: Optional[str] = data.get("node_id")
        self.git_pull_url: Optional[str] = data.get("git_pull_url")
        self.git_push_url: Optional[str] = data.get("git_push_url")
        self.html_url: Optional[str] = data.get("html_url")
        self.public: Optional[bool] = data.get("public")
        self.description: Optional[str] = data.get("description")
        self.comments: Optional[dict] = data.get("comments")
        self.comments_url: Optional[str] = data.get("comments_url")
        self.truncated: Optional[bool] = data.get("truncated")

        created_at = data.get("created_at")
        created_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S%z")
        self.created_at: Optional[datetime] = created_datetime

        updated_at = data.get("updated_at")
        updated_datetime = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S%z")
        self.updated_at: Optional[datetime] = updated_datetime

        owner = data.get("owner")
        self.owner: Optional[User] = owner if owner is None else User(owner)

        user = data.get("user")
        self.user: Optional[User] = user if user is None else User(user)

        files = data.get("files")
        self.files: Union[List[File], File] = [File.from_dict(val) for _, val in files.items()]

    async def update(self, description: Optional[str], files: Union[File, List[File]]) -> Gist:
        """
        Updates the Gist.
        There is an alias for this method, edit.

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
        return await self.client.update_gist(self.id, description, files)

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

    async def comment(self, content: str):
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

    edit = update


class Comment:
    """
    Represents a comment on a Gist.

    Attributes
    ----------
    id: Optional[:class:`int`]
        The id of the comment.
    node_id: Optional[:class:`str`]
        The node id of the comment.
    url: Optional[:class:`str`]
        The url leading to the comment.
    body: Optional[:class:`str`]
        The content of the comment.
    user: Optional:class:`User`]
        The id of the comment
    created_at: Optional[:class:`int`]
        The id of the comment
    updated_at: Optional[:class:`datetime`]
        The id of the comment
    author_association: Optional[:class:`str`]
        The type of user the commenter is to the Gist.
    """
    def __init__(self, client: Client, data: dict):
        if not data.get("id"):
            raise TypeError("Comment data must have an id.")
        self.client: Client = client
        self._set(data)

    def __repr__(self):
        return f"<Comment url={self.url}>"

    def _set(self, data: dict) -> None:
        self.id: Optional[int] = data.get("id")
        self.node_id: Optional[str] = data.get("node_id")
        self.gist_id: Optional[str] = data.get("gist_id")
        self.url: Optional[str] = data.get("url")
        self.body: Optional[str] = data.get("body")

        user = data.get("user")
        self.user: User(user)

        created_at = data.get("created_at")
        created_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S%z")
        self.created_at: Optional[datetime] = created_datetime

        updated_at = data.get("updated_at")
        updated_datetime = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S%z")
        self.updated_at: Optional[datetime] = updated_datetime

    async def delete(self) -> None:
        """
        Deletes the comment.

        Raises
        ------
        :class:`NotFound`
            The Gist or comment was not found.
        :class:`Forbidden`
            You do not have permission to delete the comment, or view the Gist.
        """
        return await self.client

    async def update(self, content: str) -> Comment:
        """
        Updates a the comment.

        Parameters
        ----------
        content: :class:`str`
            The new content of the comment.

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
        return await self.client.update_comment(self.gist_id, self.id, content)

    edit = update
