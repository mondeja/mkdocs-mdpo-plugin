"""Compendium related tests for mkdocs-mdpo-plugin."""

import os

import pytest


TESTS = (
    pytest.param(
        {
            'index.md': 'Hello\n\nHello\n',
        },
        None,
        {'languages': ['en', 'es']},
        None,
        None,
        None,
        id='repeated-messages-in-same-file',
    ),
    pytest.param(
        {
            'index.md': 'Hello\n',
            'secondary.md': 'Hello\n',
        },
        {
            'es/_compendium.po': {
                'Hello': 'Hola',
            },
        },
        {'languages': ['en', 'es']},
        {
            'nav': [
                {'Home': 'index.md'},
                {'Secondary': 'secondary.md'},
            ],
        },
        {
            'es/index.html': ['<p>Hola</p>'],
            'es/secondary/index.html': ['<p>Hola</p>'],
        },
        '#\nmsgid ""\nmsgstr ""\n\nmsgid "Hello"\nmsgstr ""\n',
        id='repeated-messages-in-different-files',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
        'expected_compendium_content',  # None would be non existent
    ),
    TESTS,
)
def test_repeated_messages_to_compendium(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    expected_compendium_content,
    mkdocs_build,
):
    """Repeated messages between different files must be dumped to the
    compendium for the language.
    """
    def after_first_build(context):
        language_dir = os.path.join(context['docs_dir'], 'es')
        compendium_filepath = os.path.join(language_dir, '_compendium.po')

        if expected_compendium_content is None:
            assert not os.path.isfile(compendium_filepath)
        else:
            assert os.path.isfile(compendium_filepath)

            with open(compendium_filepath) as f:
                assert f.read() == expected_compendium_content

    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=after_first_build,
        interrupt_after_first_build=expected_compendium_content is None,
    )
