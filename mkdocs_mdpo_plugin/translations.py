import json
import os
import re
import tempfile


class Translation:
    __slots__ = {
        'language',
        'po',
        'po_filepath',
        'po_msgids',
        'translated_msgstrs',
        'translated_msgids',
        'disabled_msgids',
    }

    def __init__(
            self,
            language,
            po,
            po_filepath,
            po_msgids,
            translated_msgstrs,
            translated_msgids,
            disabled_msgids,
    ):
        self.language = language
        self.po = po
        self.po_filepath = po_filepath
        self.po_msgids = po_msgids
        self.translated_msgstrs = translated_msgstrs
        self.translated_msgids = translated_msgids
        self.disabled_msgids = disabled_msgids

    def __str__(self):  # pragma: no cover
        return (
            f'Translation(language="{self.language}",'
            f' po=polib.POFile(...{str(len(self.po)) + " entries"}...)'
            f' po_filepath="{self.po_filepath}",'
            f' po_msgids=[...{len(self.po_msgids)} msgids...],'
            ' translated_msgstrs=['
            f'...{len(self.translated_msgstrs)} msgstrs...],'
            f' translated_msgids=[...{len(self.translated_msgids)} msgids...],'
            f' disabled_msgids=[...{len(self.disabled_msgids)} msgids...]'
            ')'
        )


class Translations:
    __slots__ = {
        'files',
        'tempdir',
        'nav',
        'compendium_files',
        'compendium_msgids',
        'compendium_msgstrs_tr',
        'current',
        'all',
    }

    def __init__(self):
        # temporal translated files created by the plugin at runtime
        # used as `self.files[file.src_path][language]``
        self.files = {}

        # temporal directory to store temporal translation files
        self.tempdir = tempfile.TemporaryDirectory(prefix='mkdocs_mdpo_')

        # navigation translation
        # {original_title: {lang: {title: [translation, url]}}}
        self.nav = {}

        # {lang: compendium_filepath}
        self.compendium_files = {}

        # {lang: [msgids]}
        self.compendium_msgids = {}

        # {lang: [msgstrs]}
        self.compendium_msgstrs_tr = {}

        # translations of current page being built
        self.current = None

        # all translations in the build
        # {lang: [Translation(...), Translation(...), ...]}
        self.all = {}

    def __str__(self):  # pragma: no cover
        current = 'None' if self.current is None else 'Translation(...)'
        return (
            f'Translations(tempdir="{self.tempdir}",'
            f' files={str(self.files)}, nav={str(self.nav)},'
            f' compendium_files={str(self.compendium_files)},'
            f' compendium_msgids={str(self.compendium_msgids)},'
            ' compendium_msgstrs_tr='
            f'{str(self.compendium_msgstrs_tr)},'
            f' current={current}'
            ')'
        )


class TranslationSearchIndexes:
    def __init__(self, site_dir, languages, default_language):
        self.site_dir = site_dir
        self.search_index_json_path = os.path.join(
            site_dir,
            'search',
            'search_index.json',
        )

        with open(self.search_index_json_path) as f:
            self.search_index_json = json.load(f)

        self.search_index = self.search_index_json['docs']

        self.languages = languages
        self.default_language = default_language

        self.lang_search_indexes = {default_language: []}  # {lang: [records]}

        self.index_loader_js = self._search_index_loader_js_filepath()

    def patch_site_dir(self):
        for language in self.languages:
            # build indexes for languages
            self.lang_search_indexes[language] = []

            if language == self.default_language:
                lang_matchers = tuple(f'{lang}/' for lang in self.languages)
                for record in self.search_index:
                    if not record['location'].startswith(lang_matchers):
                        self.lang_search_indexes[language].append(record)
            else:
                for record in self.search_index:
                    if record['location'].startswith(f'{language}/'):
                        self.lang_search_indexes[language].append(record)

            lang_search_index_path, lang_search_index = (
                self._lang_search_index_json(
                    language,
                    self.lang_search_indexes[language],
                )
            )

            # create JSON indexes
            with open(lang_search_index_path, 'w') as f:
                f.write(lang_search_index)

            # create javascript assets by language to load custom
            # search_index_{language}.json files depending on the
            # theme used

            # generate js loader for the language
            lang_index_loader_js_path, lang_index_loader_js = (
                self._lang_index_loader_js(language)
            )
            with open(lang_index_loader_js_path, 'w') as f:
                f.write(lang_index_loader_js)

        self._patch_html_files()

    def _lang_search_index_json(self, language, records):
        search_index = self.search_index_json
        search_index['docs'] = records
        if 'config' in search_index and 'lang' in search_index['config']:
            search_index['config']['lang'] = [language]
        return (
            self.search_index_json_path.rstrip('.json') + f'_{language}.json',
            json.dumps(search_index),
        )

    def _lang_index_loader_js(self, language):
        return (
            self.index_loader_js['path'].rstrip('.js') + f'_{language}.js',
            self.index_loader_js['content'].replace(
                '/search/search_index.json',
                f'/search/search_index_{language}.json',
            ),
        )

    def _patch_html_files(self):
        for root, _, files in os.walk(self.site_dir):
            for fname in files:
                if fname.endswith('.html'):
                    fpath = os.path.join(root, fname)
                    with open(fpath) as f:
                        content = f.read()
                    match = re.search(r'lang="([^"]+)"', content)
                    if match:
                        language = match.group(1)
                        index_loader_js_fname = os.path.basename(
                            self.index_loader_js['path'],
                        )
                        index_loader_js_fname_lang = (
                            index_loader_js_fname.rstrip('.js')
                            + f'_{language}.js'
                        )
                        new_content = content.replace(
                            f'assets/javascripts/{index_loader_js_fname}"',
                            (
                                'assets/javascripts/'
                                f'{index_loader_js_fname_lang}"'
                            ),
                        )
                        with open(fpath, 'w') as f:
                            f.write(new_content)

    def _search_index_loader_js_filepath(self):
        javascripts_dir = os.path.join(self.site_dir, 'assets', 'javascripts')
        js_loader_filepath, js_loader_content = None, None
        if os.path.isdir(javascripts_dir):
            for fname in os.listdir(javascripts_dir):
                if fname.endswith('.js'):
                    fpath = os.path.join(javascripts_dir, fname)
                    with open(fpath) as f:
                        content = f.read()
                    if '/search/search_index.json' in content:
                        js_loader_filepath = fpath
                        js_loader_content = content
                        continue
        return {'path': js_loader_filepath, 'content': js_loader_content}
