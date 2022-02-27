"""mdpo utilities"""

import re

from mdpo.command import COMMAND_SEARCH_REGEX


COMMAND_SEARCH_REGEX_ESCAPER = re.compile(
    (
        r'\\(' + COMMAND_SEARCH_REGEX[:20] + ')('
        + COMMAND_SEARCH_REGEX[20:38] + '?='
        + COMMAND_SEARCH_REGEX[38:] + ')'
    ),
    re.M,
)


def remove_mdpo_commands_preserving_escaped(text):
    # preserve escaped commands
    text = re.sub(
        COMMAND_SEARCH_REGEX_ESCAPER,
        r'\g<1>0-\g<2>',
        text,
    )

    text = re.sub(
        COMMAND_SEARCH_REGEX,
        '',
        text,
    )

    # restore escaped commands
    return text.replace('<!-- mdpo-0', '<!-- mdpo')
