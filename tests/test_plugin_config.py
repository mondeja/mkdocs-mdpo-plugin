"""Mkdocs builds tests for mkdocs-mdpo-plugin configuration."""

import os
from collections import OrderedDict
from tempfile import TemporaryDirectory

import mkdocs
import pytest
import yaml

from mkdocs_mdpo_plugin.plugin import MdpoPlugin


class FakeMkdocsTheme:
    def __init__(self):
        self.name = 'mkdocs'
        self._vars = {}
        self.dirs = []


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
                'Expected "languages" config setting to be a list'
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
            id='languages=undefined-theme=material-extra.alternate=[]',
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
        pytest.param(
            {
                'cross_language_search': False,
                'languages': ['en', 'es'],
            },
            {},
            mkdocs.config.base.ValidationError,
            (
                '"cross_language_search" setting is disabled but'
                ' no "search" plugin has been added to "plugins"'
            ),
            id='cross_language_search=False-plugins=[]',
        ),
        pytest.param(
            {},
            {
                'plugins': {
                    'mdpo': {
                        'cross_language_search': False,
                        'languages': [
                            'en',
                            'es',
                        ],
                    },
                    'search': {},
                },
            },
            mkdocs.config.base.ValidationError,
            (
                '"search" plugin must be placed before'
                ' "mdpo" plugin if you want to disable'
                ' "cross_language_search".'
            ),
            id='cross_language_search=False-plugins=[mdpo,search]',
        ),
        pytest.param(
            {
                'min_translated_messages': 'foo',
                'languages': [
                    'en',
                    'es',
                ],
            },
            {},
            mkdocs.config.base.ValidationError,
            (
                "The value 'foo' for 'min_translated_messages'"
                ' config setting  is not a valid percentage or'
                ' number.'
            ),
            id='min_translated_messages=foo',
        ),
        pytest.param(
            {
                'min_translated_messages': '50%',
                'languages': [
                    'en',
                    'es',
                ],
            },
            {},
            None,
            None,
            id='min_translated_messages=50%',
        ),
        pytest.param(
            {
                'min_translated_messages': 45,
                'languages': [
                    'en',
                    'es',
                ],
            },
            {},
            None,
            None,
            id='min_translated_messages=45',
        ),
        pytest.param(
            {
                'exclude': 45,
                'languages': [
                    'en',
                    'es',
                ],
            },
            {},
            mkdocs.config.base.ValidationError,
            (
                'Expected mdpo\'s "exclude" setting to be a list,'
                ' but found the value 45 of type int'
            ),
            id='exclude=<int>',
        ),
        pytest.param(
            {
                'exclude': [
                    'string',
                    45,
                ],
                'languages': [
                    'en',
                    'es',
                ],
            },
            {},
            mkdocs.config.base.ValidationError,
            (
                'Expected mdpo\'s setting "exclude[1]" value to be'
                ' a string, but found the value 45 of type int'
            ),
            id='exclude=[<str>,<int>]',
        ),
    ),
)
def test_plugin_config_errors(
    plugin_config,
    additional_config,
    expected_error_type,
    expected_error_message,
):

    with TemporaryDirectory() as site_dir, TemporaryDirectory() as docs_dir, \
            TemporaryDirectory() as config_dir:
        plugin = MdpoPlugin()
        mdpo_config = {
            'lc_messages': '',
            'locale_dir': '',
            'dest_filename_template': '{{language}}/{{file.dest_path}}',
        }
        mdpo_config.update(plugin_config)

        mkdocs_config = {
            'site_name': 'My site',
            'site_url': 'https://foo.bar',
            'docs_dir': docs_dir,
            'site_dir': site_dir,
            'plugins': OrderedDict(),
            'theme': FakeMkdocsTheme(),
        }
        if additional_config:
            if 'plugins' in additional_config:
                additional_config['plugins'] = OrderedDict(
                    additional_config['plugins'],
                )
            mkdocs_config.update(additional_config)

        _mdpo_plugin_found = False
        for plugin_name in mkdocs_config['plugins']:
            if plugin_name == 'mdpo':
                mkdocs_config['plugins'][plugin_name].update(mdpo_config)
                plugin.config = mkdocs_config['plugins'][plugin_name]
                _mdpo_plugin_found = True
                break
        if not _mdpo_plugin_found:
            mkdocs_config['plugins']['mdpo'] = mdpo_config
            plugin.config = mkdocs_config['plugins']['mdpo']

        config_filename = os.path.join(config_dir, 'mkdocs.yml')
        with open(config_filename, 'w') as f:
            yaml.dump(mkdocs_config, f)

        if expected_error_type:
            with pytest.raises(expected_error_type) as exc:
                plugin.on_config(mkdocs_config)
            assert expected_error_message in str(exc.value)
        else:
            # load configuration without errors
            plugin.on_config(mkdocs_config)
