from datetime import datetime
from typing import List


class File:
    """
    Represents a gist file.

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


class Gist:
    """
    Represents a gist.
    """

    def __init__(self, data: dict) -> None:
        self.data = data
    
    def __repr__(self) -> str:
        return f"<Gist html_url={self.data['html_url']}>"

    @property
    def url(self) -> str:
        return self.data["url"]

    @property
    def forks_url(self) -> str:
        return self.data["forks_url"]

    @property
    def commits_url(self) -> str:
        return self.data["commits_url"]

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def node_id(self) -> str:
        return self.data["node_id"]

    @property
    def git_pull_url(self) -> str:
        return self.data["git_pull_url"]

    @property
    def git_push_url(self) -> str:
        return self.data["git_push_url"]

    @property
    def html_url(self) -> str:
        return self.data["html_url"]

    @property
    def files(self) -> List[File]:
        return self.data["files"]

    @property
    def public(self) -> bool:
        return self.data["public"]

    @property
    def created_at(self) -> datetime:
        time = self.data["created_at"]
        return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")

    @property
    def updated_at(self) -> datetime:
        time = self.data["created_at"]
        return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")

    @property
    def description(self) -> str:
        return self.data["description"]

    @property
    def comments(self) -> dict:
        # returns dict for now.
        return self.data["comments"]

    @property
    def user(self) -> dict:
        # returns dict for now.
        return self.data["user"]

    @property
    def comments_url(self) -> str:
        return self.data["comments_url"]

    @property
    def owner(self) -> str:
        # returns dict for now.
        return self.data["owner"]

    @property
    def truncated(self) -> bool:
        return self.data["truncated"]


class User:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def login(self) -> str:
        return self.data["login"]

    @property
    def id(self) -> int:
        return self.data["id"]

    @property
    def node_id(self) -> str:
        return self.data["node_id"]

    @property
    def avatar_url(self) -> str:
        return self.data["avatar_url"]

    @property
    def gravatar_url(self) -> str:
        return self.data["gravatar_url"]

    @property
    def url(self) -> str:
        return self.data["url"]

    @property
    def html_url(self) -> str:
        return self.data["html_url"]

    @property
    def followers_url(self) -> str:
        return self.data["followers_url"]

    @property
    def following_url(self) -> str:
        return self.data["following_url"]

    @property
    def gists_url(self) -> str:
        return self.data["gists_url"]

    @property
    def starred_url(self) -> str:
        return self.data["starred_url"]

    @property
    def subscriptions_url(self) -> str:
        return self.data["subscriptions_url"]

    @property
    def organizations_url(self) -> str:
        return self.data["organizations_url"]

    @property
    def repos_url(self) -> str:
        return self.data["repos_url"]

    @property
    def events_url(self) -> str:
        return self.data["events_url"]

    @property
    def received_events_url(self) -> str:
        return self.data["received_events_url"]

    @property
    def type(self) -> str:
        return self.data["type"]

    @property
    def site_admin(self) -> bool:
        return self.data["site_admin"]
