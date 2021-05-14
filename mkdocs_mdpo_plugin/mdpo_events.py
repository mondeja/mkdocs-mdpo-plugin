"""Md4C parser preprocessing events for md2po instance."""

import re


try:
    from markdown.extensions.admonition import AdmonitionProcessor
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.details import DetailsProcessor
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.snippets import SnippetPreprocessor
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.tabbed import TabbedProcessor
except ImportError:  # pragma: no cover
    pass


MD2PO_EVENT_EXTENSIONS = {
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
    'link_reference': [
        'footnotes',
    ],
}

PO2MD_EVENT_EXTENSIONS = {
    'link_reference': [
        'footnotes',
    ],
}


def build_md2po_events(mkdocs_build_config):
    md_extensions = mkdocs_build_config['markdown_extensions']

    def text_event(md2po_instance, block, text):
        if 'admonition' in md_extensions:
            if re.match(AdmonitionProcessor.RE, text):
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
        if msgid.startswith(': '):
            md2po_instance._disable_next_line = True

    def link_reference_event(md2po_instance, target, *args):
        if target.startswith('^'):
            return False

    # load only those events required for the extensions
    events_functions = {
        'text': text_event,
        'msgid': msgid_event,
        'link_reference': link_reference_event,
    }

    events = {}
    for event_name, extensions in MD2PO_EVENT_EXTENSIONS.items():
        for extension in extensions:
            if extension in md_extensions:
                events[event_name] = events_functions[event_name]
                break

    return events


def build_po2md_events(mkdocs_build_config):
    md_extensions = mkdocs_build_config['markdown_extensions']

    def link_reference_event(po2md_instance, target, href, title):
        # footnotes
        if target.startswith('^'):
            # footnotes are treated as text blocks, so we don't need to
            # translate them here
            return False

    # load only those events required for the extensions
    events_functions = {
        'link_reference': link_reference_event,
    }

    events = {}
    for event_name, extensions in PO2MD_EVENT_EXTENSIONS.items():
        for extension in extensions:
            if extension in md_extensions:
                events[event_name] = events_functions[event_name]
                break

    return events
