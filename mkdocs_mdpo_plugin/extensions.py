import polib
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from mdpo.md4c import DEFAULT_MD4C_GENERIC_PARSER_EXTENSIONS

from mkdocs_mdpo_plugin.mkdocs_utils import MkdocsBuild


class MkdocsMdpoTreeProcessor(Treeprocessor):
    def run(self, root):
        mdpo_plugin = MkdocsBuild().mdpo_plugin
        tr = mdpo_plugin.translations.current
        if tr is None:
            return

        def process_translation(node, msgid):
            if msgid not in tr.translated_msgstrs:
                if msgid in tr.po_msgids:
                    for entry in tr.po:
                        if entry.msgid == msgid:
                            if entry.msgstr:
                                node.text = entry.msgstr
                                (
                                    tr.translated_msgstrs
                                ).append(
                                    entry.msgstr,
                                )
                            entry.obsolete = False
                            tr.translated_msgids.append(
                                entry.msgid,
                            )
                elif msgid not in tr.disabled_msgids:
                    tr.po_msgids.append(msgid)
                    entry = polib.POEntry(msgid=msgid, msgstr='')
                    tr.po.append(entry)

        if 'pymdownx.tasklist' in mdpo_plugin.extensions.markdown:
            node_should_be_processed = lambda node: False if (
                node.tag == 'li' and node.text[:3] in ['[ ]', '[x]', '[X]']
            ) else True

            def iterate_childs(_root):
                for child in _root:
                    # print(child.tag, child.text, child.attrib)

                    if (
                        child.text
                        and not child.text[1:].startswith('wzxhzdk:')
                    ):
                        if node_should_be_processed(child):
                            process_translation(
                                child,
                                ' '.join(child.text.split('\n')),
                            )

                    iterate_childs(child)
        else:
            def iterate_childs(_root):
                for child in _root:
                    # print(child.tag, child.text, child.attrib)

                    if (
                        child.text
                        and not child.text[1:].startswith('wzxhzdk:')
                    ):
                        process_translation(
                            child,
                            ' '.join(child.text.split('\n')),
                        )

                    iterate_childs(child)

        iterate_childs(root)


class MkdocsMdpoTitlesTreeProcessor(Treeprocessor):
    def run(self, root):
        mdpo_plugin = MkdocsBuild().mdpo_plugin

        tr = mdpo_plugin.translations.current
        if tr is None:
            return

        def process_translation(node, msgid):
            if msgid not in tr.translated_msgstrs:
                if msgid in tr.po_msgids:
                    for entry in tr.po:
                        if entry.msgid == msgid:
                            if entry.msgstr:
                                node.attrib['title'] = entry.msgstr
                                (
                                    tr.translated_msgstrs
                                ).append(
                                    entry.msgstr,
                                )
                            entry.obsolete = False
                            tr.translated_msgids.append(
                                entry.msgid,
                            )
                elif msgid not in tr.disabled_msgids:
                    tr.po_msgids.append(msgid)
                    entry = polib.POEntry(msgid=msgid, msgstr='')
                    tr.po.append(entry)

        if 'abbr' in mdpo_plugin.extensions.markdown:
            if 'pymdownx.emoji' in mdpo_plugin.extensions.markdown:
                node_should_be_processed = lambda node: (
                    node.tag != 'abbr' and
                    node.get('class') not in ['emojione', 'twemoji', 'gemoji']
                )
            else:
                node_should_be_processed = lambda node: node.tag != 'abbr'
        elif 'pymdownx.emoji' in mdpo_plugin.extensions.markdown:
            node_should_be_processed = lambda node: (
                node.get('class') not in ['emojione', 'twemoji', 'gemoji']
            )

        if (
            'abbr' in mdpo_plugin.extensions.markdown
            or 'pymdownx.emoji' in mdpo_plugin.extensions.markdown
        ):
            def iterate_childs(_root):
                for child in _root:
                    # print("TITLE", child.tag, child.text, child.attrib)

                    if 'title' in child.attrib and 'mdpo' not in child.attrib:
                        if node_should_be_processed(child):
                            process_translation(
                                child,
                                child.attrib['title'],
                            )
                    iterate_childs(child)
        else:
            def iterate_childs(_root):
                for child in _root:
                    # print("TITLE", child.tag, child.text, child.attrib)

                    if 'title' in child.attrib and 'mdpo' not in child.attrib:
                        process_translation(
                            child,
                            child.attrib['title'],
                        )
                    iterate_childs(child)

        iterate_childs(root)


class MkdocsMdpoExtension(Extension):
    def extendMarkdown(self, md):
        # run first
        md.treeprocessors.register(
            MkdocsMdpoTreeProcessor(self),
            'mkdocs-mdpo-tree',
            88888,
        )

        # run latest
        md.treeprocessors.register(
            MkdocsMdpoTitlesTreeProcessor(self),
            'mkdocs-mdpo-tree-titles',
            -88888,
        )


class Extensions:  # pragma: no cover
    __slots__ = {
        'markdown',
        'md4c',
    }

    def __init__(self):
        # markdown extensions used by the build (loaded on config event)
        self.markdown = None

        # md4c extensions used in mdpo translation (depend on Python-Markdown
        # configured extensions in `mkdocs.yml`)
        self.md4c = DEFAULT_MD4C_GENERIC_PARSER_EXTENSIONS
