"""Translations search indexes tests."""

import json
import os

import pytest


TESTS = (
    pytest.param(  # mkdocs theme
        {
            'index.md': (
                'Foo'
            ),
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'cross_language_search': False,
        },
        {
            'plugins': [
                {
                    'search': {},
                },
            ],
        },
        {
            'index.html': [
                '<p>Foo</p>',
            ],
            'es/index.html': [
                '<p>Foo es</p>',
            ],
            'search/main_en.js': [
                'worker_en.js',
            ],
            'search/main_es.js': [
                'worker_es.js',
            ],
            'search/worker_en.js': [
                'search_index_en.json',
            ],
            'search/worker_es.js': [
                'search_index_es.json',
            ],
        },
        id='mkdocs',
    ),
    pytest.param(  # readthedocs theme
        {
            'index.md': (
                'Foo'
            ),
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'cross_language_search': False,
        },
        {
            'plugins': [
                {
                    'search': {},
                },
            ],
            'theme': {
                'name': 'readthedocs',
            },
        },
        {
            'index.html': [
                '<p>Foo</p>',
                'search_en.html',
            ],
            'es/index.html': [
                '<p>Foo es</p>',
                'search_es.html',
            ],
            'search/main_en.js': [
                'worker_en.js',
            ],
            'search/main_es.js': [
                'worker_es.js',
            ],
            'search/worker_en.js': [
                'search_index_en.json',
            ],
            'search/worker_es.js': [
                'search_index_es.json',
            ],
            'search_en.html': [
                'search_en.html',
            ],
            'search_es.html': [
                'search_es.html',
            ],
        },
        id='readthedocs',
    ),
    pytest.param(  # material theme
        {
            'index.md': (
                'Foo'
            ),
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'cross_language_search': False,
        },
        {
            'plugins': [
                {
                    'search': {},
                },
            ],
            'theme': {
                'name': 'material',
            },
        },
        {
            'index.html': [
                '<p>Foo</p>',
                '_en.js',
            ],
            'es/index.html': [
                '<p>Foo es</p>',
                '_es.js',
            ],
        },
        id='material',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
    ),
    TESTS,
)
def test_search_indexes(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    mkdocs_build,
):
    def check_search_indexes(context):
        search_dir = os.path.join(context['site_dir'], 'search')

        for fname in os.listdir(search_dir):
            if fname.endswith('index.json') or not fname.endswith('.json'):
                continue
            fpath = os.path.join(search_dir, fname)
            with open(fpath) as f:
                search_index = json.loads(f.read())

            language = fname.split('_')[-1].split('.')[0]

            assert isinstance(search_index, dict)
            assert isinstance(language, str)
            assert len(search_index) > 0

            if language == plugin_config['languages'][0]:       # en
                other_language = plugin_config['languages'][1]  # es
                for record in search_index['docs']:
                    assert not record['location'].startswith(
                        (f'{language}/', f'{other_language}/'),
                    )
            else:
                for record in search_index['docs']:
                    assert record['location'].startswith(f'{language}/')

    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=check_search_indexes,
    )
