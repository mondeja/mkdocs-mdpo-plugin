import functools


def readable_float(number):
    if str(number).endswith('.0'):
        number = int(number)
    round_number = str(round(number, 2))
    if len(round_number) != len(str(number)):
        round_number = f'~{round_number}'
    return round_number


def removepreffix(s, pref):
    if pref and s.startswith(pref):
        return s[len(pref):]
    return s


def removesuffix(s, suf):
    if suf and s.endswith(suf):
        return s[:-len(suf)]
    return s


def po_messages_stats(po):
    untranslated_messages, total_messages = 0, 0

    for entry in po:
        total_messages += 1
        if not entry.msgstr and not entry.obsolete:
            untranslated_messages += 1
    return (
        total_messages - untranslated_messages,
        total_messages,
    )


@functools.lru_cache(maxsize=None)
def get_package_version(pkg):
    try:
        from importlib import metadata
    except ImportError:
        try:
            import importlib_metadata as metadata  # python < 3.8
        except ImportError:
            try:
                import pkg_resources
            except ImportError:
                return None
            else:
                return pkg_resources.get_distribution(pkg).version
        else:
            return metadata.version(pkg)
    else:
        return metadata.version(pkg)
