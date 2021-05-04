"""Mkdocs builds tests for mkdocs-mdpo-plugin configuration."""

import pytest


tests = (
    (
        # basic example with default configuration
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        {
            'default_language': 'en',
            'languages': ['en', 'es'],
        },
        None,
        {
            'index.html': [
                '<h1 id="foo">Foo</h1>',
                '<p>bar</p></div>',
            ],
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # nested files
        {
            'index.md': 'foo\n',
            'foo/bar/baz.md': 'hello\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
            'es/foo/bar/baz.md.po': {
                'Baz': 'Baz es',  # added by default Mkdocs theme to dropdown
                'hello': 'hola',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
            'foo/bar/baz/index.html': ['<p>hello</p>'],
            'es/foo/bar/baz/index.html': ['<p>hola</p>'],
        },
    ),
    (
        # custom locale_dir
        {
            'index.md': 'foo\n',
        },
        {
            'locales/es/index.md.po': {
                'foo': 'foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'locale_dir': 'locales',
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # custom dest_filename_template
        {
            'index.md': 'foo\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'locale_dir': '',
            'dest_filename_template': (
                '{{page.file.dest_path|replace(".html", "")}}-'
                '{{language}}.html'
            ),
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index-es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # custom locale_dir + dest_filename_template
        {
            'index.md': 'foo\n',
        },
        {
            'locales/es/index.md.po': {
                'foo': 'foo es',
            },
        },
        {
            'locale_dir': 'locales',
            'languages': ['en', 'es'],
            'dest_filename_template':
            '{{page.file.dest_path|replace(".html", "")}}_{{language}}.html',
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index_es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # configuration from 'material' theme
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        None,
        {
            'theme': {
                'name': 'material',
                'language': 'en',
            },
            'extra': {
                'alternate': [
                    {
                        'name': 'English',
                        'lang': 'en',
                    },
                    {
                        'name': 'Español',
                        'link': 'es',
                        'lang': 'es',
                    },
                ],
            },
        },
        {
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # boolean lc_messages
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/LC_MESSAGES/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        {
            'languages': ['en', 'es'],
            'lc_messages': True,
        },
        None,
        {
            'index.html': [
                '<h1 id="foo">Foo</h1>',
                '<p>bar</p></div>',
            ],
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # custom lc_messages
        {
            'index.md': 'foo\n',
        },
        {
            'es/barbaz/index.md.po': {
                'foo': 'foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'lc_messages': 'barbaz',
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # title translation
        {
            'index.md': 'foo\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
                'Introduction': 'Introducción',
            },
        },
        {
            'languages': ['en', 'es'],

        },
        {
            'nav': [
                {'Introduction': 'index.md'},
            ],
        },
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': [
                '<p>foo es</p>',
                '<title>Introducción - My site</title>',
            ],
        },
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
    tests,
)
def test_config(
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
