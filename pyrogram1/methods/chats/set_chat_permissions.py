#  Pyrogram1 - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram1.
#
#  Pyrogram1 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram1 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram1.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

from pyrogram1 import raw
from pyrogram1 import types
from pyrogram1.scaffold import Scaffold


class SetChatPermissions(Scaffold):
    async def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: "types.ChatPermissions",
    ) -> "types.Chat":
        """Set default chat permissions for all members.

        You must be an administrator in the group or a supergroup for this to work and must have the
        *can_restrict_members* admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            permissions (:obj:`~pyrogram1.types.ChatPermissions`):
                New default chat permissions.

        Returns:
            :obj:`~pyrogram1.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from pyrogram1.types import ChatPermissions

                # Completely restrict chat
                app.set_chat_permissions(chat_id, ChatPermissions())

                # Chat members can only send text messages and media messages
                app.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True
                    )
                )
        """

        r = await self.send(
            raw.functions.messages.EditChatDefaultBannedRights(
                peer=await self.resolve_peer(chat_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=0,
                    send_messages=not permissions.can_send_messages,
                    send_media=not permissions.can_send_media_messages,
                    send_stickers=not permissions.can_send_other_messages,
                    send_gifs=not permissions.can_send_other_messages,
                    send_games=not permissions.can_send_other_messages,
                    send_inline=not permissions.can_send_other_messages,
                    embed_links=not permissions.can_add_web_page_previews,
                    send_polls=not permissions.can_send_polls,
                    change_info=not permissions.can_change_info,
                    invite_users=not permissions.can_invite_users,
                    pin_messages=not permissions.can_pin_messages,
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])