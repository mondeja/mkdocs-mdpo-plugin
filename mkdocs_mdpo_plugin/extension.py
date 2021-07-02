import polib
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from mkdocs_mdpo_plugin.plugin import MkdocsBuild


class MkdocsMdpoTreeProcessor(Treeprocessor):
    def run(self, root):
        mdpo_plugin = MkdocsBuild().mdpo_plugin

        current_page = mdpo_plugin.current_page
        if not hasattr(current_page, '_language'):
            return

        def process_translation(node, msgid):
            if msgid not in current_page._translated_entries_msgstrs:
                if msgid in current_page._po_msgids:
                    for entry in current_page._po:
                        if entry.msgid == msgid:
                            if entry.msgstr:
                                node.text = entry.msgstr
                                (
                                    current_page._translated_entries_msgstrs
                                ).append(
                                    entry.msgstr,
                                )
                            entry.obsolete = False
                            current_page._translated_entries_msgids.append(
                                entry.msgid,
                            )
                elif msgid not in current_page._disabled_msgids:
                    current_page._po_msgids.append(msgid)
                    entry = polib.POEntry(msgid=msgid, msgstr='')
                    current_page._po.append(entry)

        if 'pymdownx.tasklist' in mdpo_plugin._markdown_extensions:
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
        current_page._po.save(current_page._po_filepath)


class MkdocsMdpoTitlesTreeProcessor(Treeprocessor):
    def run(self, root):
        mdpo_plugin = MkdocsBuild().mdpo_plugin

        current_page = mdpo_plugin.current_page
        if not hasattr(current_page, '_language'):
            return

        def process_translation(node, msgid):
            if msgid not in current_page._translated_entries_msgstrs:
                if msgid in current_page._po_msgids:
                    for entry in current_page._po:
                        if entry.msgid == msgid:
                            if entry.msgstr:
                                node.attrib['title'] = entry.msgstr
                                (
                                    current_page._translated_entries_msgstrs
                                ).append(
                                    entry.msgstr,
                                )
                            entry.obsolete = False
                            current_page._translated_entries_msgids.append(
                                entry.msgid,
                            )
                elif msgid not in current_page._disabled_msgids:
                    current_page._po_msgids.append(msgid)
                    entry = polib.POEntry(msgid=msgid, msgstr='')
                    current_page._po.append(entry)

        if 'abbr' in mdpo_plugin._markdown_extensions:
            if 'pymdownx.emoji' in mdpo_plugin._markdown_extensions:
                node_should_be_processed = lambda node: (
                    node.tag != 'abbr' and
                    node.get('class') not in ['emojione', 'twemoji', 'gemoji']
                )
            else:
                node_should_be_processed = lambda node: node.tag != 'abbr'
        elif 'pymdownx.emoji' in mdpo_plugin._markdown_extensions:
            node_should_be_processed = lambda node: (
                node.get('class') not in ['emojione', 'twemoji', 'gemoji']
            )

        if (
            'abbr' in mdpo_plugin._markdown_extensions
            or 'pymdownx.emoji' in mdpo_plugin._markdown_extensions
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

        current_page._po.save(current_page._po_filepath)


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
