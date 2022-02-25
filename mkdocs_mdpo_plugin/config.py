"""Configuration event for 'mkdocs-mdpo-plugin'."""

from mkdocs.config.base import ValidationError
from mkdocs.config.config_options import Type


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

    # store reference in plugin to markdown_extensions for later usage
    plugin.extensions.markdown = markdown_extensions

    # ----------------------------------------------------------
