"""Tests for 'translate' config setting."""

import os

import pytest


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
        'expected_compendium_files_content',
    ),
    (
        pytest.param(
            {
                'index.md': (
                    'Hello\n\nBye'
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
                'translate': ['site_name'],
            },
            {
                'site_name': 'The name of the site',
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                ],
            },
            {
                'es/_compendium.po': [
                    'msgid "The name of the site"',
                ],
            },
            id='translate=[site_name]',
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
                    'Bye': 'Adiós',
                },
            },
            {
                'languages': ['en', 'es'],
                'translate': ['site_name', 'site_description'],
            },
            {
                'site_name': 'The name of the site',
                'site_description': 'The description of the site',
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                ],
            },
            {
                'es/_compendium.po': [
                    'msgid "The name of the site"',
                    'msgid "The description of the site"',
                ],
            },
            id='translate=[site_name,site_description]',
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
                    'Bye': 'Adiós',
                },
                'fr/index.md.po': {
                    'Hello': 'Salut',
                    'Bye': 'Adieu',
                },
            },
            {
                'languages': ['en', 'es', 'fr'],
                'translate': ['site_name', 'site_description'],
            },
            {
                'site_name': 'The name of the site',
                'site_description': 'The description of the site',
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                ],
                'fr/index.html': [
                    '<p>Salut</p>',
                    '<p>Adieu</p>',
                ],
            },
            {
                'es/_compendium.po': [
                    'msgid "The name of the site"',
                    'msgid "The description of the site"',
                ],
                'fr/_compendium.po': [
                    'msgid "The name of the site"',
                    'msgid "The description of the site"',
                ],
            },
            id='translate=[site_name,site_description]-languages[en,es,fr]',
        ),
    ),
)
def test_translate_dumped_to_compendium(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    expected_compendium_files_content,
    mkdocs_build,
):
    def check_config_settings_dumped_to_compendium(context):
        for relpath, contents in expected_compendium_files_content.items():
            fpath = os.path.join(context['docs_dir'], relpath)
            with open(fpath) as f:
                compendium_content = f.read()
            for content in contents:
                assert content in compendium_content, (
                    f'Expected "{content}" inside {fpath} but not found'
                )

    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=check_config_settings_dumped_to_compendium,
        interrupt_after_first_build=True,
    )


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
    ),
    (
        pytest.param(
            {
                'index.md': (
                    'Hello\n\nBye'
                ),
            },
            {
                'es/index.md.po': {
                    'Hello': 'Hola',
                    'Bye': 'Adiós',
                },
                'es/_compendium.po': {
                    'The name of the site': 'El nombre del sitio',
                },
            },
            {
                'languages': ['en', 'es'],
                'translate': ['site_name'],
            },
            {
                'site_name': 'The name of the site',
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                    'El nombre del sitio',
                ],
            },
            id='translate=[site_name]',
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
                    'Bye': 'Adiós',
                },
                'es/_compendium.po': {
                    'The description of the site': 'La descripción del sitio',
                },
            },
            {
                'languages': ['en', 'es'],
                'translate': ['site_description'],
            },
            {
                'site_name': 'The name of the site',
                'site_description': 'The description of the site',
                'theme': {
                    'name': 'material',
                    # TODO: mkdocs theme does not recognize 'es/index.html'
                    #       as homepage with `.is_homepage`?
                },
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                    'The name of the site',
                    'La descripción del sitio',
                ],
            },
            id='translate=[site_description]',
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
                    'Bye': 'Adiós',
                },
                'es/_compendium.po': {
                    'The name of the site': 'El nombre del sitio',
                    'The description of the site': 'La descripción del sitio',
                },
            },
            {
                'languages': ['en', 'es'],
                'translate': ['site_name', 'site_description'],
            },
            {
                'site_name': 'The name of the site',
                'site_description': 'The description of the site',
                'theme': {
                    'name': 'material',
                },
            },
            {
                'es/index.html': [
                    '<p>Hola</p>',
                    '<p>Adiós</p>',
                    'El nombre del sitio',
                    'La descripción del sitio',
                ],
            },
            id='translate=[site_name,site_description]',
        ),
    ),
)
def test_translate_html_output(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    mkdocs_build,
):
    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
    )
