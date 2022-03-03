"""Tests for "min_translated_messages" configuration setting."""

import os

import pytest


TESTS = (
    pytest.param(
        {
            'index.md': (
                'Hello\n\nBye'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': '',
            },
        },
        {
            'languages': ['en', 'es'],
            'min_translated_messages': '50%',
        },
        {},
        {
            'index.html': [
                '<p>Hello</p>',
                '<p>Bye</p>',
            ],
        },
        (
            'Excluding language "es". Translated 0% (0 of 3 messages)'
            ' but required 50% at least.'
        ),
        (
            'Excluding language "es". Translated ~33.33% (1 of 3 messages)'
            ' but required 50% at least.'
        ),
        id='min_translated_messages=50%',
    ),
    pytest.param(
        {
            'index.md': (
                'Hello\n\nBye'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': '',
            },
        },
        {
            'languages': ['en', 'es'],
            'min_translated_messages': 2,
        },
        {},
        {
            'index.html': [
                '<p>Hello</p>',
                '<p>Bye</p>',
            ],
        },
        (
            'Excluding language "es". Translated 0 messages of'
            ' 3 but required 2 translated messages at least.'
        ),
        (
            'Excluding language "es". Translated 1 messages of'
            ' 3 but required 2 translated messages at least.'
        ),
        id='min_translated_messages=2',
    ),
    pytest.param(
        {
            'index.md': (
                'Hello\n\nBye'
            ),
            'changelog.md': (
                'Some changes\n\nIn the changelog'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': '',
            },
        },
        {
            'languages': ['en', 'es'],
            'min_translated_messages': 2,
            'exclude': ['changelog.md'],
        },
        {},
        {
            'index.html': [
                '<p>Hello</p>',
                '<p>Bye</p>',
            ],
            'changelog/index.html': [
                '<p>Some changes</p>',
                '<p>In the changelog</p>',
            ],
        },
        (
            'Excluding language "es". Translated 0 messages of'
            ' 3 but required 2 translated messages at least.'
        ),
        (
            'Excluding language "es". Translated 1 messages of'
            ' 3 but required 2 translated messages at least.'
        ),
        id='min_translated_messages=2-exclude=[changelog.md]',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
        'expected_first_build_log',
        'expected_second_build_log',
    ),
    TESTS,
)
def test_min_translated_messages(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    expected_first_build_log,
    expected_second_build_log,
    mkdocs_build,
):
    def check_translated_files_not_exists(context):
        es_path = os.path.join(context['site_dir'], 'es')
        es_index_path = os.path.join(es_path, 'index.html')
        assert not os.path.exists(es_path)
        assert not os.path.exists(es_index_path)

    _, plugin_log = mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=check_translated_files_not_exists,
        allow_missing_translations=True,
    )

    # first build log
    assert expected_first_build_log in plugin_log

    # second build log
    assert expected_second_build_log in (
        plugin_log.split(expected_first_build_log)[-1]  # after first build log
    )
