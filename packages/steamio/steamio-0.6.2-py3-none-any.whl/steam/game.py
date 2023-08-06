# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2020 James

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import functools
from datetime import timedelta
from typing import Any, Callable, Optional, TypeVar, Union, overload

from typing_extensions import TypedDict

from .enums import IntEnum

__all__ = (
    "TF2",
    "Game",
    "CSGO",
    "DOTA2",
    "STEAM",
    "CUSTOM_GAME",
)

T = TypeVar("T")
APP_ID_MAX = 2 ** 32
GAMES: dict[int, list[Game]] = {}


class Games(IntEnum):
    Team_Fortress_2 = 440
    DOTA_2 = 570
    Counter_Strike_Global__Offensive = 730
    Steam = 753


class GameDict(TypedDict):
    name: str
    appid: str
    playtime_forever: int
    img_icon_url: str
    img_logo_url: str
    has_community_visible_stats: bool


class GameToDict(TypedDict, total=False):
    game_id: str
    game_extra_info: str


def cache_values(new: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(new)
    def inner(*args: Any, **kwargs: Any) -> T:
        game = new(*args, **kwargs)

        try:
            games = GAMES[game.id]
        except KeyError:
            GAMES[game.id] = games = [game]

        for game_ in games:
            if game_.title == game.title:
                return game_

        return game

    return inner


class Game:
    """Represents a Steam game.

    Note
    ----
    This class can be defined by users using the above parameters, or it can be from an API call this is when
    :meth:`~steam.User.fetch_games` is called.

    Parameters
    ----------
    title: Optional[:class:`str`]
        The game's title.
    id: Optional[:class:`int`]
        The game's app ID.
    context_id: Optional[:class:`int`]
        The game's context ID by default 2.

    Attributes
    -----------
    title: Optional[:class:`str`]
        The game's title.
    id: :class:`int`
        The game's app ID.
    context_id: :class:`int`
        The context id of the game normally ``2``.
    total_play_time: :class:`datetime.timedelta`
        The total time the game has been played for.
        Only applies to a :class:`~steam.User`'s games from :meth:`~steam.User.games`.
    icon_url: Optional[:class:`str`]
        The icon url of the game.
        Only applies to a :class:`~steam.User`'s games from :meth:`~steam.User.games`.
    logo_url: Optional[:class:`str`]
        The logo url of the game.
        Only applies to a :class:`~steam.User`'s games from :meth:`~steam.User.games`.
    """

    __slots__ = (
        "id",
        "title",
        "context_id",
        "total_play_time",
        "icon_url",
        "logo_url",
        "_stats_visible",
    )

    id: int
    title: Optional[str]
    context_id: Optional[int]

    total_play_time: Optional[timedelta]
    icon_url: Optional[str]
    logo_url: Optional[str]
    _stats_visible: Optional[bool]

    @overload
    def __new__(cls, *, id: Union[int, str], context_id: Optional[int] = None) -> Game:
        ...

    @overload
    def __new__(cls, *, title: str, context_id: Optional[int] = None) -> Game:
        ...

    @overload
    def __new__(cls, *, id: Union[int, str], title: str, context_id: Optional[int] = None) -> Game:
        ...

    @overload
    def __new__(
        cls, *, id: Optional[Union[int, str]] = None, title: Optional[str] = None, context_id: Optional[int] = None
    ) -> Game:
        ...

    @cache_values
    def __new__(
        cls, *, id: Optional[Union[int, str]] = None, title: Optional[str] = None, context_id: Optional[int] = None
    ) -> Game:
        if title is None and id is None:
            raise TypeError("__new__() missing a required keyword argument: 'id' or 'title'")

        self = super().__new__(cls)

        if title is None:
            try:
                id = int(id)
            except (ValueError, TypeError):
                raise ValueError(f"id expected to support int()")
            try:
                title = Games(id).name.replace("__", "-").replace("_", " ")
            except ValueError:
                title = None
            else:
                if title == "Steam" and context_id is None:
                    context_id = 6
        elif id is None:
            try:
                id = Games[title.replace(" ", "_").replace("-", "__")].value
            except KeyError:
                id = 0
        else:
            try:
                id = int(id)
            except (ValueError, TypeError):
                raise ValueError("id must be an int") from None

        if id < 0:
            raise ValueError("id cannot be negative")

        self.id = id
        self.title = title
        self.context_id = 2 if context_id is None else context_id

        self.total_play_time = None
        self.icon_url = None
        self.logo_url = None
        self._stats_visible = None

        return self

    @classmethod
    def _from_api(cls, data: GameDict) -> Game:
        game = cls(id=data.get("appid"), title=data.get("name"))
        game.total_play_time = timedelta(minutes=data.get("playtime_forever", 0))
        game.icon_url = (
            f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{game.id}/"
            f"{data.get('img_icon_url')}.jpg"
        )
        game.logo_url = (
            f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{game.id}"
            f"/{data.get('img_logo_url')}.jpg"
        )
        game._stats_visible = data.get("has_community_visible_stats", False)
        return game

    def __str__(self) -> str:
        return self.title or ""

    def __repr__(self) -> str:
        attrs = ("title", "id", "context_id")
        resolved = [f"{attr}={getattr(self, attr)!r}" for attr in attrs]
        return f"Game({', '.join(resolved)})"

    def to_dict(self) -> GameToDict:
        """dict[:class:`str`, :class:`str`]: The dict representation of the game used to set presences."""
        return (
            {"game_id": str(self.id)}
            if self.is_steam_game()
            else {"game_id": str(self.id), "game_extra_info": self.title}
        )

    def is_steam_game(self) -> bool:
        """:class:`bool`: Whether the game could be a Steam game."""
        return self.id <= APP_ID_MAX

    def has_visible_stats(self) -> bool:
        """:class:`bool`: Whether the game has publicly visible stats.
        Only applies to a :class:`~steam.User`'s games from :meth:`~steam.User.games`.
        """
        return self._stats_visible


TF2 = Game(title="Team Fortress 2")
DOTA2 = Game(title="DOTA 2")
CSGO = Game(title="Counter Strike Global-Offensive")
STEAM = Game(title="Steam", context_id=6)


def CUSTOM_GAME(title: str) -> Game:
    """Create a custom game instance for :meth:`~steam.Client.change_presence`.
    The :attr:`Game.id` will be set to ``15190414816125648896`` and the :attr:`Game.context_id` to ``None``.

    Example: ::

        await client.change_presence(game=steam.CUSTOM_GAME('my cool game'))

    Parameters
    ----------
    title: :class:`str`
        The name of the game to set your playing status to.

    Returns
    -------
    class:`Game`
        The created custom game.
    """
    return Game(title=title, id=15190414816125648896, context_id=None)
