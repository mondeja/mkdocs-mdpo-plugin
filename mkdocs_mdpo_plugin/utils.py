def readable_float(number):
    if str(number).endswith('.0'):
        number = int(number)
    round_number = str(round(number, 2))
    if len(round_number) != len(str(number)):
        round_number = f'~{round_number}'
    return round_number


def removesuffix(s, suf):
    if suf and s.endswith(suf):
        return s[:-len(suf)]
    return s


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
    )
