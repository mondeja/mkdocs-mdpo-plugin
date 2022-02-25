"""Mkdocs builds tests for mkdocs-mdpo-plugin configuration."""

import os
from tempfile import TemporaryDirectory

import mkdocs
import pytest
import yaml

from mkdocs_mdpo_plugin.plugin import MdpoPlugin


tests = (
    pytest.param(  # basic example with default configuration
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
        id='default-config',
    ),
    pytest.param(  # nested files
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
        id='nested-files',
    ),
    pytest.param(  # custom locale_dir
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
        id='custom-locale_dir',
    ),
    pytest.param(  # custom dest_filename_template
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
                '{{file.dest_path|replace(".html", "")}}-'
                '{{language}}.html'
            ),
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index-es.html': ['<p>foo es</p>'],
        },
        id='custom-dest_filename_template',
    ),
    pytest.param(  # custom locale_dir + dest_filename_template
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
            '{{file.dest_path|replace(".html", "")}}_{{language}}.html',
        },
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index_es.html': ['<p>foo es</p>'],
        },
        id='custom-locale_dir+dest_filename_template',
    ),
    pytest.param(  # configuration from 'material' theme
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
        id='material-theme',
    ),
    pytest.param(  # boolean lc_messages
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
        id='bool-lc_messages',
    ),
    pytest.param(  # custom lc_messages
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
        id='custom-lc_messages',
    ),
    pytest.param(  # nav title translation
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
        id='nav-title-translation',
    ),
    pytest.param(  # ignore msgids
        {
            'index.md': 'foo\n\nbar\n\nbaz\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
        },
        {
            'languages': ['en', 'es'],
            'ignore_msgids': ['bar', 'baz'],
        },
        None,
        {
            'index.html': [
                '<p>foo</p>',
                '<p>bar</p>',
                '<p>baz</p>',
            ],
            'es/index.html': [
                '<p>foo es</p>',
                '<p>bar</p>',
                '<p>baz</p>',
            ],
        },
        id='ignore_msgids',
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
def test_plugin_config(
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


@pytest.mark.parametrize(
    (
        'plugin_config',
        'additional_config',
        'expected_error_type',
        'expected_error_message',
    ),
    (
        pytest.param(
            {
                'languages': 5,
            },
            None,
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using the 'plugins.mdpo.languages' configuration"
                ' setting.'
            ),
            id='languages=<int>',
        ),
        pytest.param(
            {
                'default_language': 'es',
            },
            {
                'theme': type(
                    'Theme', (), {
                        'name': 'readthedocs',
                    },
                ),
            },
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using the 'plugins.mdpo.languages' configuration"
                ' setting.'
            ),
            id='languages=undefined-theme=readthedocs',
        ),
        pytest.param(
            {
                'default_language': 'es',
            },
            {
                'theme': type(
                    'Theme', (), {
                        'name': 'material',
                    },
                ),
            },
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using either 'plugins.mdpo.languages' or"
                " 'extra.alternate' configuration settings."
            ),
            id='languages=undefined-theme=material-extra=undefined',
        ),
        pytest.param(
            {
                'default_language': 'es',
            },
            {
                'theme': type(
                    'Theme', (), {
                        'name': 'material',
                    },
                ),
                'extra': {
                    'alternate': [],
                },
            },
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using either 'plugins.mdpo.languages' or"
                " 'extra.alternate' configuration settings."
            ),
            id='languages=undefined-theme=material-extra.alternate=undefined',
        ),
        pytest.param(
            {
                'default_language': 'es',
            },
            {
                'theme': type(
                    'Theme', (), {
                        'name': 'material',
                    },
                ),
                'extra': {
                    'alternate': [],
                },
            },
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using either 'plugins.mdpo.languages' or"
                " 'extra.alternate' configuration settings."
            ),
            id='languages=undefined-theme=material-extra.alternate=undefined',
        ),
        pytest.param(
            {},
            {
                'theme': type(
                    'Theme', (), {
                        'name': 'material',
                    },
                ),
            },
            mkdocs.config.base.ValidationError,
            (
                'You must define the languages you will translate the content'
                " into using either 'plugins.mdpo.languages' or"
                " 'extra.alternate' configuration settings."
            ),
            id='languages=undefined-theme=material',
        ),
    ),
)
def test_plugin_config_errors(
    plugin_config,
    additional_config,
    expected_error_type,
    expected_error_message,
    caplog,
):

    with TemporaryDirectory() as site_dir, TemporaryDirectory() as docs_dir, \
            TemporaryDirectory() as config_dir:
        plugin = MdpoPlugin()
        mdpo_config = {
            'lc_messages': '',
            'locale_dir': '',
            'dest_filename_template': '{{language}}/{{page.file.dest_path}}',
        }
        mdpo_config.update(plugin_config)

        plugin.config = mdpo_config

        mkdocs_config = {
            'site_name': 'My site',
            'site_url': 'https://foo.bar',
            'docs_dir': docs_dir,
            'site_dir': site_dir,
            'plugins': [
                {'mdpo': mdpo_config},
            ],
        }
        if additional_config:
            mkdocs_config.update(additional_config)

        config_filename = os.path.join(config_dir, 'mkdocs.yml')
        with open(config_filename, 'w') as f:
            yaml.dump(mkdocs_config, f)

        if expected_error_type is mkdocs.exceptions.ConfigurationError:
            with pytest.raises(expected_error_type) as exc:
                mkdocs.config.load_config(config_filename)
            assert 'Aborted with 1 Configuration Errors!' in str(exc)

            assert len(caplog.records) == 1
            error_log = caplog.records[0]
            assert error_log.args[0] == 'plugins'

            error = error_log.args[1]
            assert isinstance(error, mkdocs.config.base.ValidationError)

            error_message = error.args[0]
            assert error_message == expected_error_message
        else:
            with pytest.raises(expected_error_type) as exc:
                plugin.on_config(mkdocs_config)
