import pytest


TESTS = (
    pytest.param(  # material theme
        {
            'index.md': (
                '---\ndescription: "Description"\n---\n\nFoo'
            ),
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'Description': 'Descripción',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'theme': {
                'name': 'material',
            },
        },
        {
            'index.html': [
                '<p>Foo</p>',
                '<meta name="description" content="Description"',
            ],
            'es/index.html': [
                '<p>Foo es</p>',
                '<meta name="description" content="Descripción"',
            ],
        },
        id='theme=material',
    ),
    pytest.param(  # mkdocs theme (not added with metadata)
        {
            'index.md': (
                '---\ndescription: "Description"\n---\n\nFoo'
            ),
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'Description': 'Descripción',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {},
        {
            'index.html': [
                '<p>Foo</p>',
                '</title>\n',
            ],
            'es/index.html': [
                '<p>Foo es</p>',
            ],
        },
        id='theme=mkdocs',
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
def test_metadata_translation(
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
