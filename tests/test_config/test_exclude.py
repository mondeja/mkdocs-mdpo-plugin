"""Tests for "exclude" configuration setting."""

import os

import pytest


TESTS = (
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
                'Bye': 'Adiós',
            },
        },
        {
            'languages': ['en', 'es'],
            'exclude': ['changelog.md'],
        },
        {},
        {
            'es/index.html': [
                '<p>Hola</p>',
                '<p>Adiós</p>',
            ],
            'es/changelog/index.html': [
                '<p>Some changes</p>',
                '<p>In the changelog</p>',
            ],
        },
        ['es/changelog.md.po'],
        id='languages=[en,es]-exclude=[changelog.md]',
    ),
    pytest.param(
        {
            'index.md': (
                'Hello\n\nBye'
            ),
            'changelog1.md': (
                'Some changes 1\n\nIn the changelog 1'
            ),
            'changelog2.md': (
                'Some changes 2\n\nIn the changelog 2'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': 'Adiós',
            },
            'fr/index.md.po': {
                'Hello': 'Salut',
                'Bye': 'Adieu',
            },
        },
        {
            'languages': ['en', 'es', 'fr'],
            'exclude': ['changelog1.md', 'changelog2.md'],
        },
        {},
        {
            'es/index.html': [
                '<p>Hola</p>',
                '<p>Adiós</p>',
            ],
            'es/changelog1/index.html': [
                '<p>Some changes 1</p>',
                '<p>In the changelog 1</p>',
            ],
            'fr/changelog1/index.html': [
                '<p>Some changes 1</p>',
                '<p>In the changelog 1</p>',
            ],
            'es/changelog2/index.html': [
                '<p>Some changes 2</p>',
                '<p>In the changelog 2</p>',
            ],
            'fr/changelog2/index.html': [
                '<p>Some changes 2</p>',
                '<p>In the changelog 2</p>',
            ],
        },
        [
            'es/changelog1.md.po',
            'es/changelog2.md.po',
            'fr/changelog1.md.po',
            'fr/changelog2.md.po',
        ],
        id='languages=[en,es,fr]-exclude=[changelog1.md,changelog2.md]',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
        'unexistent_files',
    ),
    TESTS,
)
def test_exclude(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    unexistent_files,
    mkdocs_build,
):
    def check_po_translation_files_not_exists(context):
        for unexistent_file in unexistent_files:
            fpath = os.path.join(context['docs_dir'], unexistent_file)
            assert not os.path.exists(fpath)

    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=check_po_translation_files_not_exists,
    )
