#  RSS to Telegram Bot
#  Copyright (C) 2022-2024  Rongrong <i@rong.moe>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from typing import Union

import asyncio
from aiohttp import ClientError
from telethon.errors import (
    UserIsBlockedError, UserIdInvalidError, ChatWriteForbiddenError, ChannelPrivateError, InputUserDeactivatedError,
    PhotoInvalidDimensionsError, PhotoSaveFileInvalidError, PhotoInvalidError, PhotoCropSizeSmallError,
    PhotoContentUrlEmptyError, PhotoContentTypeInvalidError, GroupedMediaInvalidError, MediaGroupedInvalidError,
    MediaInvalidError, VideoContentTypeInvalidError, VideoFileInvalidError, ExternalUrlInvalidError,
    WebpageCurlFailedError, WebpageMediaEmptyError, MediaEmptyError, ChatAdminRequiredError, ChatRestrictedError
)


class EntityNotFoundError(ValueError):
    def __init__(self, peer: Union[int, str]):
        self.peer = peer
        super().__init__(f"Entity not found: {peer}")


class ContextTimeoutError(asyncio.TimeoutError):
    pass


class TopicUnavailableError(Exception):
    """
    Raised when a post could not be sent to the forum topic a sub is bound to.

    Telegram rejects sending to a closed topic, but silently drops the reply to a deleted one, sending the post to
    the chat itself instead. The latter is detected after the fact, thus this error is not an RPC error.
    """

    def __init__(self, topic_id: int, reason: str):
        self.topic_id = topic_id
        self.reason = reason
        super().__init__(f'Topic {topic_id} is unavailable: {reason}')


UserBlockedErrors: tuple = (UserIsBlockedError, UserIdInvalidError, ChatWriteForbiddenError, ChannelPrivateError,
                            InputUserDeactivatedError, ChatAdminRequiredError, EntityNotFoundError, ChatRestrictedError)
InvalidMediaErrors: tuple = (PhotoInvalidDimensionsError, PhotoSaveFileInvalidError, PhotoInvalidError,
                             PhotoCropSizeSmallError, PhotoContentUrlEmptyError, PhotoContentTypeInvalidError,
                             GroupedMediaInvalidError, MediaGroupedInvalidError, MediaInvalidError,
                             VideoContentTypeInvalidError, VideoFileInvalidError, ExternalUrlInvalidError)
ExternalMediaFetchFailedErrors: tuple = (WebpageCurlFailedError, WebpageMediaEmptyError, MediaEmptyError)
MediaSendFailErrors = InvalidMediaErrors + ExternalMediaFetchFailedErrors


class RetryInIpv4(ClientError):
    def __init__(self, code: int = None, reason: str = None):
        self.code = code
        self.reason = reason
        super().__init__(f'{code} {reason}' if code and reason else (code or reason or ''))
