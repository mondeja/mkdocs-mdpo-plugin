"""mdpo utilities"""

import re

from mdpo.command import COMMAND_SEARCH_REGEX


STRIP_COMMAND_REGEX = re.compile(r'[^\\]' + COMMAND_SEARCH_REGEX)


def remove_mdpo_commands_preserving_escaped(text):
    # preserve escaped commands
    text = re.sub(
        r'(\\<!--\s*mdpo)',
        r'\g<1>-0',
        text,
    )

    text = re.sub(
        STRIP_COMMAND_REGEX,
        '',
        text,
    )

    # restore escaped commands
    return re.sub(
        r'\\<!--\s*mdpo-0',
        '<!-- mdpo',
        text,
    )
