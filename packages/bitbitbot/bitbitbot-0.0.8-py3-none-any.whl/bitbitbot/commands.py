from typing import Optional

from bitbitbot.models import Role

COMMANDS: dict[str, callable] = {}


def command(command_name: str, permission: Role = Role.VIEWER) -> callable:
    def _permissioned(func: callable) -> callable:
        def _func_wrapper(bot, msg, tags) -> callable:
            if tags.role <= permission:
                func(bot, msg, tags)
        COMMANDS[command_name] = _func_wrapper
        return _func_wrapper
    return _permissioned
