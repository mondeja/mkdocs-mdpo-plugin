"""Translation search indexes used to restrict the search index to
the current language for each page in site directory.

The patch implies several steps, which depend on the active theme:

1. Get 'search_index.json' or equivalent file path. Ussually located
   at 'search/search_index.json'.
2. Separate original search index which includes all the records
   for all the languages in different search indexes, one per language.
   The files are named 'search_index_es.json', 'search_index_fr.json'...
3. Patch the JS files which loads the 'search_index.json' file creating
   one for each language. This depends completely on the active theme.
4. Patch HTML page files to load these language versions of JS files
   instead of the original ones.
5. Additionally, for themes like readthedocs, patchs HTML search files.
"""

import copy
import json
import os

from mkdocs_mdpo_plugin.utils import removesuffix


def _language_extension_path(path, extension, language, separator='_'):
    return f'{path[:-len(extension)]}{separator}{language}{extension}'

##
# Get worker Javascript files.
##


def _material_get_worker_js_files(site_dir):
    worker_js_filepath, worker_js_content = None, None
    javascripts_dir = os.path.join(site_dir, 'assets', 'javascripts')
    for fname in os.listdir(javascripts_dir):
        if fname.endswith('.js'):
            fpath = os.path.join(javascripts_dir, fname)
            with open(fpath) as f:
                content = f.read()
            if '/search/search_index.json' in content:
                worker_js_filepath = fpath
                worker_js_content = content
                continue
    return [{'path': worker_js_filepath, 'content': worker_js_content}]


def _mkdocs_get_worker_js_files(site_dir):
    worker_js_filepath = os.path.join(site_dir, 'search', 'worker.js')
    with open(worker_js_filepath) as f:
        worker_js_content = f.read()

    main_js_filepath = os.path.join(site_dir, 'search', 'main.js')
    with open(main_js_filepath) as f:
        main_js_content = f.read()

    return [
        {'path': worker_js_filepath, 'content': worker_js_content},
        {'path': main_js_filepath, 'content': main_js_content},
    ]


THEME_WORKER_FILES_FUNCS = {
    'material': _material_get_worker_js_files,
    'mkdocs': _mkdocs_get_worker_js_files,
    'readthedocs': _mkdocs_get_worker_js_files,
}

##
# Patch Javascript worker files.
##


def _material_patch_worker_js_files(files, language):
    worker_js = files[0]
    new_path = _language_extension_path(worker_js['path'], '.js', language)

    new_content = worker_js['content'].replace(
        '/search/search_index.json',
        f'/search/search_index_{language}.json',
    )
    with open(new_path, 'w') as f:
        f.write(new_content)


def _mkdocs_patch_worker_js_files(files, language):
    worker_js, main_js = files

    new_worker_js_path = _language_extension_path(
        worker_js['path'],
        '.js',
        language,
    )
    new_worker_js_content = worker_js['content'].replace(
        'search_index.json',
        f'search_index_{language}.json',
    )
    with open(new_worker_js_path, 'w') as f:
        f.write(new_worker_js_content)

    new_main_js_path = _language_extension_path(
        main_js['path'],
        '.js',
        language,
    )
    new_main_js_content = main_js['content'].replace(
        'worker.js',
        f'worker_{language}.js',
    )
    with open(new_main_js_path, 'w') as f:
        f.write(new_main_js_content)


THEME_WORKER_PATCHS_FUNCS = {
    'material': _material_patch_worker_js_files,
    'mkdocs': _mkdocs_patch_worker_js_files,
    'readthedocs': _mkdocs_patch_worker_js_files,
}

##
# Patch HTML files to load language JS worker files.
##


def _material_patch_html_file(fpath, language, worker_files):
    with open(fpath) as f:
        content = f.read()

    worker_js_fname = os.path.basename(worker_files[0]['path'])
    worker_js_fname_lang = _language_extension_path(
        worker_js_fname,
        '.js',
        language,
    )

    new_content = content.replace(
        f'assets/javascripts/{worker_js_fname}"',
        f'assets/javascripts/{worker_js_fname_lang}"',
    )
    with open(fpath, 'w') as f:
        f.write(new_content)


def _mkdocs_patch_html_file(fpath, language, *args):
    with open(fpath) as f:
        content = f.read()

    new_content = content.replace(
        'search/main.js',
        f'search/main_{language}.js',
    )
    with open(fpath, 'w') as f:
        f.write(new_content)


THEME_HTML_PATCHS_FUNCS = {
    'material': _material_patch_html_file,
    'mkdocs': _mkdocs_patch_html_file,
    'readthedocs': _mkdocs_patch_html_file,
}

##
# Get search files
##


def _readthedocs_get_search_files(site_dir):
    search_file_path = os.path.join(site_dir, 'search.html')
    with open(search_file_path) as f:
        search_file_content = f.read()
    return [{'path': search_file_path, 'content': search_file_content}]


THEME_GET_SEARCH_FILES_FUNCS = {
    'readthedocs': _readthedocs_get_search_files,
}

##
# Patch search files
##


def _reathedocs_patch_search_files(
        fpath,
        language,
        default_language,
        search_files,
):
    search_file = search_files[0]

    # create search file for the language if not exists
    lang_search_path = _language_extension_path(
        search_file['path'],
        '.html',
        language,
    )
    lang_search_path_content = search_file['content'].replace(
        'search.html',
        f'search_{language}.html',
    ).replace(
        f'search/main_{default_language}.js',
        f'search/main_{language}.js',
    )
    with open(lang_search_path, 'w') as f:
        f.write(lang_search_path_content)

    # patch search file URL in language file
    with open(fpath) as f:
        content = f.read()
    new_content = content.replace(
        'search.html',
        f'search_{language}.html',
    )
    with open(fpath, 'w') as f:
        f.write(new_content)


THEME_PATCH_SEARCH_FILES_FUNCS = {
    'readthedocs': _reathedocs_patch_search_files,
}

##
# Update 'search_index.json#config.lang' only for some themes:
##

THEME_ALTER_SEARCH_INDEX_LANG_CONFIG = [
    'material',
]


class TranslationsSearchPatcher:
    supported_themes = THEME_WORKER_FILES_FUNCS.keys()

    def __init__(
            self,
            site_dir,
            languages,
            default_language,
            theme_name,
            locations,
    ):
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
        self.theme_name = theme_name

        # map from locations of files to languages
        self.locations = locations

        # {lang: [records]}
        self.lang_search_indexes = {language: [] for language in languages}

        # worker files which load search indexes
        self.worker_js_files = THEME_WORKER_FILES_FUNCS[self.theme_name](
            self.site_dir,
        )
        for js_file in self.worker_js_files:
            if None in js_file.values():
                raise OSError(
                    'The search worker file can not be retrieved from'
                    f' site directory {self.site_dir}',
                )

    def patch_site_dir(self):
        # build indexes for languages
        for record in self.search_index:
            if not record['location']:
                self.lang_search_indexes[self.default_language].append(record)
            elif '#' in record['location']:
                if record['location'].startswith('#'):
                    self.lang_search_indexes[self.default_language].append(
                        record,
                    )
                else:
                    clean_location = record['location'].split('#')[0]
                    if clean_location in self.locations:
                        language = self.locations[clean_location]
                        self.lang_search_indexes[language].append(record)
            elif record['location'] in self.locations:
                language = self.locations[record['location']]
                self.lang_search_indexes[language].append(record)

        # get site directory HTML files ordered by language
        html_files_by_language = self._get_html_files_by_language()

        for language in self.languages:
            # create indexes for languages
            self._create_lang_search_index_json(
                language,
                self.lang_search_indexes[language],
            )

            # create javascript assets by language to load custom
            # search_index_{language}.json files depending on the
            # active theme

            # patch Javascript worker files for the language
            THEME_WORKER_PATCHS_FUNCS[self.theme_name](
                self.worker_js_files,
                language,
            )

            # patch HTML files to load localized assets
            for fpath in html_files_by_language[language]:
                THEME_HTML_PATCHS_FUNCS[self.theme_name](
                    fpath,
                    language,
                    self.worker_js_files,
                )

        # if the theme needs to patch search files, patch them
        if self.theme_name in THEME_GET_SEARCH_FILES_FUNCS:
            search_files = THEME_GET_SEARCH_FILES_FUNCS[self.theme_name](
                self.site_dir,
            )
            for language in self.languages:
                for fpath in html_files_by_language[language]:
                    THEME_PATCH_SEARCH_FILES_FUNCS[self.theme_name](
                        fpath,
                        language,
                        self.default_language,
                        search_files,
                    )

    def _create_lang_search_index_json(self, language, records):
        search_index = copy.copy(self.search_index_json)
        search_index['docs'] = records
        if (
                self.theme_name in THEME_ALTER_SEARCH_INDEX_LANG_CONFIG
                and 'config' in search_index
                and 'lang' in search_index['config']
        ):
            search_index['config']['lang'] = [language]

        new_path = _language_extension_path(
            self.search_index_json_path,
            '.json',
            language,
        )
        with open(new_path, 'w') as f:
            f.write(json.dumps(search_index))

    def _get_html_files_by_language(self):
        language_files = {language: [] for language in self.languages}

        for root, _, files in os.walk(self.site_dir):
            for fname in [f for f in files if f.endswith('.html')]:
                fpath = os.path.join(root, fname)
                relpath = os.path.relpath(fpath, self.site_dir)
                location = removesuffix(relpath, 'index.html')
                if location in self.locations:
                    language = self.locations[location]
                    language_files[language].append(fpath)
                else:
                    language_files[self.default_language].append(fpath)
        return language_files
