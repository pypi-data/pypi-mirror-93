from enum import IntEnum
from typing import Optional

from pydantic import BaseModel


class Role(IntEnum):
    BROADCASTER = 0
    MODERATOR = 1
    SUBSCRIBER = 2
    VIEWER = 3


class TwitchTags(BaseModel):
    display_name: str
    color: Optional[str]
    user_id: str
    broadcaster: bool = False
    mod: bool
    subscriber: bool
    role: Role = Role.VIEWER

    def __init__(self, **data):
        super().__init__(**data)

        if self.mod:
            self.role = Role.MODERATOR
        elif self.subscriber:
            self.role = Role.SUBSCRIBER

        if 'broadcaster' in data.get('badges', ''):
            self.broadcaster = True
            self.role = Role.BROADCASTER
