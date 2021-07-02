"""Configuration event for 'mkdocs-mdpo-plugin'."""

import mkdocs


def on_config_event(plugin, config, **kwargs):
    """Configuration event for 'mkdocs-mdpo-plugin'.

    * Define properly `lc_messages`, `languages` and `locale_dir`
      configuration settings.
    * Loads `mkdocs.mdpo` extension.
    * Configures md4c extensions accordingly to Python-Markdown extensions.
    * Stores the Markdown extensions used in the build in the
      ``_markdown_extensions`` property of the plugin instance.
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
        return mkdocs.config.base.ValidationError(msg)

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
            if 'tables' in plugin._md4c_extensions:
                plugin._md4c_extensions.remove('tables')
        else:
            if 'tables' not in plugin._md4c_extensions:
                plugin._md4c_extensions.append('tables')
        if 'wikilinks' not in markdown_extensions:
            if 'wikilinks' in plugin._md4c_extensions:
                plugin._md4c_extensions.remove('wikilinks')
        else:
            if 'wikilinks' not in plugin._md4c_extensions:
                plugin._md4c_extensions.append('wikilinks')

        # spaces after '#' are optional in Python-Markdown for headers,
        # but the extension 'pymdownx.saneheaders' makes them mandatory
        if 'pymdownx.saneheaders' in markdown_extensions:
            if 'permissive_atx_headers' in plugin._md4c_extensions:
                plugin._md4c_extensions.remove('permissive_atx_headers')
        else:
            if 'permissive_atx_headers' not in plugin._md4c_extensions:
                plugin._md4c_extensions.append('permissive_atx_headers')

        # 'pymdownx.tasklist' enables 'tasklists' MD4C extentsion
        if 'pymdownx.tasklist' in markdown_extensions:
            if 'tasklists' not in plugin._md4c_extensions:
                plugin._md4c_extensions.append('tasklists')
        else:
            if 'tasklists' in plugin._md4c_extensions:
                plugin._md4c_extensions.remove('tasklists')

        # 'pymdownx.tilde' enables strikethrough syntax, but only works
        # if the MD4C extension is disabled
        if 'pymdownx.tilde' in markdown_extensions:
            if 'strikethrough' in plugin._md4c_extensions:
                plugin._md4c_extensions.remove('strikethrough')

        # configure internal 'mkdocs.mdpo' extension
        if 'mkdocs.mdpo' in markdown_extensions:  # pragma: no cover
            config['markdown_extensions'].remove('mkdocs.mdpo')
        config['markdown_extensions'].append('mkdocs.mdpo')

    # store reference in plugin to markdown_extensions for later usage
    plugin._markdown_extensions = markdown_extensions

    # ----------------------------------------------------------
