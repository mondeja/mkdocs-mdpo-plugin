"""mdpo utilities"""

import re

from mdpo.command import COMMAND_SEARCH_REGEX


COMMAND_SEARCH_REGEX_AT_LINE_START = re.compile(
    r'^(\s{2,})?[^\\]' + COMMAND_SEARCH_REGEX + r'\n?',
    re.M,
)
COMMAND_SEARCH_REGEX_ESCAPER = re.compile(
    (
        r'\\(' + COMMAND_SEARCH_REGEX[:20] + ')('
        + COMMAND_SEARCH_REGEX[20:38] + '?='
        + COMMAND_SEARCH_REGEX[38:] + ')'
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
            COMMAND_SEARCH_REGEX_AT_LINE_START,
            '',
            # preserve escaped commands
            re.sub(
                COMMAND_SEARCH_REGEX_ESCAPER,
                r'\g<1>0-\g<2>',
                text,
            ),
        ),
    )


def po_messages_stats(pofile_content):
    untranslated_messages, total_messages = -1, -1
    content_lines = pofile_content.splitlines()

    for i, line in enumerate(content_lines):
        next_i = i + 1

        if line.startswith('msgid "'):
            total_messages += 1

        if line.startswith('msgstr ""') and (
            next_i == len(content_lines) or (not content_lines[next_i].strip())
        ):
            untranslated_messages += 1

    return (
        total_messages - untranslated_messages,
        total_messages,
        # (total_messages - untranslated_messages) / total_messages * 100,
    )
