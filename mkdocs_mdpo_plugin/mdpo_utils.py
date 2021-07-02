"""mdpo utilities"""

import re

from mdpo.command import COMMAND_SEARCH_RE


COMMAND_SEARCH_RE_AT_LINE_START = re.compile(
    r'^(\s{2,})?[^\\]' + COMMAND_SEARCH_RE.pattern + r'\n?',
    re.M,
)
COMMAND_SEARCH_RE_ESCAPER = re.compile(
    (
        r'\\(' + COMMAND_SEARCH_RE.pattern[:20] + ')('
        + COMMAND_SEARCH_RE.pattern[20:38] + '?='
        + COMMAND_SEARCH_RE.pattern[38:] + ')'
    ),
    re.M,
)


def remove_mdpo_commands_preserving_escaped(text):
    return re.sub(
        # restore escaped commands
        '<!-- mdpo-0',
        '<!-- mdpo',
        re.sub(
            # remove commands
            COMMAND_SEARCH_RE_AT_LINE_START,
            '',
            # preserve escaped commands
            re.sub(
                COMMAND_SEARCH_RE_ESCAPER,
                r'\g<1>0-\g<2>',
                text,
            ),
        ),
    )
