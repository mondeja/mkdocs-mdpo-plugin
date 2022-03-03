"""Configuration event for 'mkdocs-mdpo-plugin'."""

import logging
import os

from mkdocs.config.base import ValidationError
from mkdocs.config.config_options import Type

from mkdocs_mdpo_plugin import __file__ as installation_path
from mkdocs_mdpo_plugin.mkdocs_utils import get_lunr_languages


logger = logging.getLogger('mkdocs.plugins.mdpo')


CONFIG_SCHEME = (
    ('locale_dir', Type(str, default='')),
    ('default_language', Type(str, required=False)),
    ('languages', Type(list, required=False)),
    ('lc_messages', Type((str, bool), default='')),
    (
        'dest_filename_template',
        Type(str, default='{{language}}/{{file.dest_path}}'),
    ),
    ('ignore_extensions', Type(list, default=['.po', '.pot', '.mo'])),
    ('ignore_msgids', Type(list, default=[])),
    ('cross_language_search', Type(bool, default=True)),
    ('min_translated_messages', Type((str, int), default=None)),
    ('exclude', Type(list, default=[])),
    ('translate', Type(list, default=[])),
)


def on_config_event(plugin, config, **kwargs):
    """Configuration event for 'mkdocs-mdpo-plugin'.

    * Define properly `lc_messages`, `languages` and `locale_dir`
      configuration settings.
    * Loads `mkdocs-mdpo` extension.
    * Configures md4c extensions accordingly to Python-Markdown extensions.
    * Stores the Markdown extensions used in the build in the
      ``extensions.markdown`` property of the plugin instance.
    * Creates the persistent files cache for the project.
    """
    if plugin.config['lc_messages'] is True:
        plugin.config['lc_messages'] = 'LC_MESSAGES'
    elif not plugin.config['lc_messages']:
        plugin.config['lc_messages'] = ''

    try:
        _using_material_theme = config['theme'].name == 'material'
    except KeyError:
        _using_material_theme = None

    # load language selection settings from material or mdpo configuration
    def _languages_required():
        msg = (
            'You must define the languages you will translate the'
            ' content into using'
            f"{' either' if _using_material_theme else ' the'}"
            " 'plugins.mdpo.languages'"
        )
        if _using_material_theme:
            msg += " or 'extra.alternate'"
        msg += (
            ' configuration setting'
            f"{'s' if _using_material_theme else ''}."
        )
        return ValidationError(msg)

    languages = plugin.config.get('languages')
    if not languages:
        if _using_material_theme:
            if 'extra' not in config:
                raise _languages_required()
            alternate = config['extra'].get('alternate')
            if not alternate:
                raise _languages_required()
            plugin.config['languages'] = [alt['lang'] for alt in alternate]
        else:
            raise _languages_required()
    else:
        if not isinstance(languages, list):
            raise ValidationError(
                'Expected "languages" config setting to be a list',
            )
        for i, language in enumerate(languages):
            if not isinstance(language, str):
                raise ValidationError(
                    f'Expected "languages[{i}]" config setting to'
                    f' be a string but is {language}',
                )

    default_language = plugin.config.get('default_language')
    if not default_language:
        # use mkdocs>=v1.2.0 theme localization setting
        theme_locale = (
            None if 'theme' not in config
            else config['theme']._vars.get('locale')
        )
        if theme_locale and theme_locale in plugin.config['languages']:
            plugin.config['default_language'] = theme_locale
        else:
            if (
                not isinstance(plugin.config['languages'], list)
                or not plugin.config['languages']
            ):
                raise _languages_required()

            plugin.config['default_language'] = plugin.config['languages'][0]

    # ----------------------------------------------------------

    # extensions configuration
    markdown_extensions = config.get('markdown_extensions')

    # configure MD4C extensions
    if markdown_extensions:
        if 'tables' not in markdown_extensions:
            if 'tables' in plugin.extensions.md4c:
                plugin.extensions.md4c.remove('tables')
        else:
            if 'tables' not in plugin.extensions.md4c:
                plugin.extensions.md4c.append('tables')
        if 'wikilinks' not in markdown_extensions:
            if 'wikilinks' in plugin.extensions.md4c:
                plugin.extensions.md4c.remove('wikilinks')
        else:
            if 'wikilinks' not in plugin.extensions.md4c:
                plugin.extensions.md4c.append('wikilinks')

        # spaces after '#' are optional in Python-Markdown for headers,
        # but the extension 'pymdownx.saneheaders' makes them mandatory
        if 'pymdownx.saneheaders' in markdown_extensions:
            if 'permissive_atx_headers' in plugin.extensions.md4c:
                plugin.extensions.md4c.remove('permissive_atx_headers')
        else:
            if 'permissive_atx_headers' not in plugin.extensions.md4c:
                plugin.extensions.md4c.append('permissive_atx_headers')

        # 'pymdownx.tasklist' enables 'tasklists' MD4C extentsion
        if 'pymdownx.tasklist' in markdown_extensions:
            if 'tasklists' not in plugin.extensions.md4c:
                plugin.extensions.md4c.append('tasklists')
        else:
            if 'tasklists' in plugin.extensions.md4c:
                plugin.extensions.md4c.remove('tasklists')

        # 'pymdownx.tilde' enables strikethrough syntax, but only works
        # if the MD4C extension is disabled
        if 'pymdownx.tilde' in markdown_extensions:
            if 'strikethrough' in plugin.extensions.md4c:
                plugin.extensions.md4c.remove('strikethrough')

        # configure internal 'mkdocs-mdpo' extension
        if 'mkdocs-mdpo' in markdown_extensions:  # pragma: no cover
            config['markdown_extensions'].remove('mkdocs-mdpo')
        config['markdown_extensions'].append('mkdocs-mdpo')

    # install a i18n aware version of sitemap.xml if not provided by the user
    theme_custom_dir = config['theme']._vars.get('custom_dir', '.')
    if not os.path.isfile(os.path.join(theme_custom_dir, 'sitemap.xml')):
        custom_sitemap_dir = os.path.join(
            os.path.dirname(installation_path),
            'custom_mdpo_sitemap',
        )
        config['theme'].dirs.insert(0, custom_sitemap_dir)

    # check that cross language search configuration is valid
    if plugin.config.get('cross_language_search') is False:
        if 'search' not in config['plugins']:
            raise ValidationError(
                '"cross_language_search" setting is disabled but'
                ' no "search" plugin has been added to "plugins"',
            )
        else:
            plugin_names = [p for p in config['plugins']]
            if plugin_names.index('search') > plugin_names.index('mdpo'):
                raise ValidationError(
                    '"search" plugin must be placed before "mdpo"'
                    ' plugin if you want to disable "cross_language_search".',
                )
    elif not _using_material_theme and 'search' in config['plugins']:
        # if cross_language_search is active, add all languages to 'search'
        # plugin configuration
        lunr_languages = get_lunr_languages()
        search_langs = config['plugins']['search'].config.get('lang', [])
        for language in plugin.config['languages']:
            if language in lunr_languages:
                if language not in search_langs:
                    config['plugins']['search'].config['lang'].append(
                        language,
                    )
                    logger.debug(
                        f"[mdpo] Adding '{language}' to"
                        " 'plugins.search.lang' option",
                    )
            elif language != 'en':  # English does not need steemer
                logger.info(
                    f"[mdpo] Language '{language}' is not supported by"
                    " lunr.js, not adding it to 'plugins.search.lang'"
                    ' option',
                )

    # check that minimum translated messages required for each language
    # is a valid value
    min_translated = plugin.config.get('min_translated_messages')
    if min_translated is not None:
        try:
            if '%' in str(min_translated):
                min_translated = max(-100, -float(min_translated.strip('%')))
            else:
                min_translated = max(int(min_translated), 0)
        except Exception:
            raise ValidationError(
                f"The value '{min_translated}' for"
                " 'min_translated_messages' config setting"
                '  is not a valid percentage or number.',
            )
        else:
            plugin.config['min_translated_messages'] = min_translated

    # check that 'exclude' contains a valid list
    exclude = plugin.config.get('exclude', [])
    if not isinstance(exclude, list):
        raise ValidationError(
            'Expected mdpo\'s "exclude" setting to be a list, but found'
            f' the value {str(exclude)} of type {type(exclude).__name__}',
        )
    else:
        for i, path in enumerate(exclude):
            if not isinstance(path, str):
                raise ValidationError(
                    f'Expected mdpo\'s setting "exclude[{i}]" value to'
                    f' be a string, but found the value {str(path)} of'
                    f' type {type(path).__name__}',
                )
    plugin.config['exclude'] = exclude

    # translation of configuration settings
    valid_translate_settings = ['site_name', 'site_description']
    for setting in plugin.config.get('translate', []):
        if setting not in valid_translate_settings:
            valid_translate_settings_readable = ' and '.join([
                f"'{opt}'" for opt in valid_translate_settings
            ])
            raise ValidationError(
                f"The setting '{setting}' is not supported for"
                " 'plugins.mdpo.translate' config setting. Valid settings"
                f' are {valid_translate_settings_readable}',
            )
        elif (
            setting == 'site_description'
            and not config.get('site_description')
        ):
            logger.warn(
                '[mdpo] "site_description" is configured to be translated'
                ' but was not defined in mkdocs.yml',
            )
            plugin.config['translate'].remove('site_description')

    # store reference in plugin to markdown_extensions for later usage
    plugin.extensions.markdown = markdown_extensions

    # ----------------------------------------------------------
