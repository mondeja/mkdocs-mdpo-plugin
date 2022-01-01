"""Md4C parser preprocessing events for md2po instance."""

import re  # noqa: F401


try:
    from markdown.extensions.admonition import (  # noqa: F401
        AdmonitionProcessor,
    )
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.details import DetailsProcessor  # noqa: F401
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.snippets import SnippetPreprocessor  # noqa: F401
except ImportError:  # pragma: no cover
    pass
try:
    from pymdownx.tabbed import TabbedProcessor  # noqa: F401
except ImportError:  # pragma: no cover
    pass
try:
    from mkdocstrings.extension import (  # noqa: F401
        AutoDocProcessor as MkDocsStringsProcessor,
        MkdocstringsExtension,
    )
except ImportError:  # pragma: no cover
    pass


PO2MD_EVENT_EXTENSIONS = {
    'link_reference': [
        'footnotes',
    ],
}


def build_md2po_events(markdown_extensions):
    """Build dinamically those mdpo events executed at certain moments of the
    Markdown file parsing extrating messages from pages, different depending on
    active extensions and plugins.
    """
    md_extensions = []
    for ext in markdown_extensions:
        if not isinstance(ext, str):
            if isinstance(ext, MkdocstringsExtension):
                md_extensions.append('mkdocstrings')
            else:
                md_extensions.append(ext)
        else:
            md_extensions.append(ext)

    def build_event(event_type):
        parameters = {
            'text': 'md2po_instance, block, text',
            'msgid': 'md2po_instance, msgid, *args',
            'link_reference': 'md2po_instance, target, *args',
        }[event_type]

        if event_type == 'text':
            req_extension_conditions = {
                'admonition': 're.match(AdmonitionProcessor.RE, text)',
                'pymdownx.details': 're.match(DetailsProcessor.START, text)',
                'pymdownx.snippets': (
                    're.match(SnippetPreprocessor.RE_ALL_SNIPPETS, text)'
                ),
                'pymdownx.tabbed': 're.match(TabbedProcessor.START, text)',
                'mkdocstrings': 're.match(MkDocsStringsProcessor.regex, text)',
            }

            body = ''
            for req_extension, condition in req_extension_conditions.items():
                if req_extension in md_extensions:
                    body += (
                        f'    if {condition}:\n        '
                        'md2po_instance.disabled_entries.append(text)\n'
                        '        return False\n'
                    )
            if not body:
                return None
        elif event_type == 'msgid':
            body = (
                "    if msgid.startswith(': '):"
                'md2po_instance.disable_next_block = True\n'
            )
        else:  # link_reference
            body = "    if target.startswith('^'):return False;\n"

        function_definition = f'def {event_type}_event({parameters}):\n{body}'
        code = compile(function_definition, 'test', 'exec')
        exec(code)
        return locals()[f'{event_type}_event']

    # load only those events required for the extensions
    events_functions = {
        event:
        build_event(event) for event in ['text', 'msgid', 'link_reference']
    }

    events = {}
    for event_name, event_function in events_functions.items():
        if event_function is not None:
            events[event_name] = event_function

    return events


def build_po2md_events(markdown_extensions):
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
            if extension in markdown_extensions:
                events[event_name] = events_functions[event_name]
                break

    return events
