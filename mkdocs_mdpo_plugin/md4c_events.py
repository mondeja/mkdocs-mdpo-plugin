"""Md4C parser preprocessing events for md2po instance."""

import re


try:
    from markdown.extensions.admonition import AdmonitionProcessor
except ImportError:
    pass
try:
    from markdown.extensions.def_list import DefListProcessor
    DEF_LIST_RE = re.compile(DefListProcessor.RE.pattern.replace('{1', '{2'))
except ImportError:
    pass
try:
    from pymdownx.details import DetailsProcessor
except ImportError:
    pass
try:
    from pymdownx.snippets import SnippetPreprocessor
except ImportError:
    pass
try:
    from pymdownx.tabbed import TabbedProcessor
except ImportError:
    pass


EVENT_EXTENSIONS = {
    'text': [
        'admonition',
        'def_list',
        'pymdownx.details',
        'pymdownx.snippets',
        'pymdownx.tabbed',
    ],
    'msgid': [
        'def_list',
    ],
}


def build_md4c_parser_events(mkdocs_build_config):
    md_extensions = mkdocs_build_config['markdown_extensions']

    def text_event(md2po_instance, block, text):
        if 'admonition' in md_extensions:
            if re.match(AdmonitionProcessor.RE, text):
                md2po_instance.disabled_entries.append(text)
                return False
        if 'def_list' in md_extensions:
            if re.match(DEF_LIST_RE, text):
                md2po_instance.disabled_entries.append(text)
                return False
        if 'pymdownx.details' in md_extensions:
            if re.match(DetailsProcessor.START, text):
                md2po_instance.disabled_entries.append(text)
                return False
        if 'pymdownx.snippets' in md_extensions:
            if re.match(SnippetPreprocessor.RE_ALL_SNIPPETS, text):
                md2po_instance.disabled_entries.append(text)
                return False
        if 'pymdownx.tabbed' in md_extensions:
            if re.match(TabbedProcessor.START, text):
                md2po_instance.disabled_entries.append(text)
                return False

    def msgid_event(md2po_instance, msgid):
        if 'def_list' in md_extensions:
            if msgid.startswith(': '):
                md2po_instance._disable_next_line = True

    # load only those events required for the extensions
    events_functions = {
        'text': text_event,
        'msgid': msgid_event,
    }

    events = {}
    for event_name, extensions in EVENT_EXTENSIONS.items():
        for extension in extensions:
            if extension in md_extensions:
                events[event_name] = events_functions[event_name]
                break

    return events
