import tempfile


class Translation:
    __slots__ = {
        'language',
        'po',
        'po_filepath',
        'po_msgids',
        'translated_msgstrs',
        'translated_msgids',
        'disabled_msgids',
    }

    def __init__(
            self,
            language,
            po,
            po_filepath,
            po_msgids,
            translated_msgstrs,
            translated_msgids,
            disabled_msgids,
    ):
        self.language = language
        self.po = po
        self.po_filepath = po_filepath
        self.po_msgids = po_msgids
        self.translated_msgstrs = translated_msgstrs
        self.translated_msgids = translated_msgids
        self.disabled_msgids = disabled_msgids

    def __str__(self):  # pragma: no cover
        return (
            f'Translation(language="{self.language}",'
            f' po=polib.POFile(...{str(len(self.po)) + " entries"}...)'
            f' po_filepath="{self.po_filepath}",'
            f' po_msgids=[...{len(self.po_msgids)} msgids...],'
            ' translated_msgstrs=['
            f'...{len(self.translated_msgstrs)} msgstrs...],'
            f' translated_msgids=[...{len(self.translated_msgids)} msgids...],'
            f' disabled_msgids=[...{len(self.disabled_msgids)} msgids...]'
            ')'
        )


class Translations:
    __slots__ = {
        'files',
        'tempdir',
        'nav',
        'compendium_files',
        'compendium_msgids',
        'compendium_msgstrs_tr',
        'current',
        'all',
        'locations',
        'stats',
        'config_settings',
    }

    def __init__(self):
        # temporal translated files created by the plugin at runtime
        # used as `self.files[file.src_path][language]``
        self.files = {}

        # temporal directory to store temporal translation files
        self.tempdir = tempfile.TemporaryDirectory(prefix='mkdocs_mdpo_')

        # navigation translation
        # {original_title: {lang: {title: [translation, url]}}}
        self.nav = {}

        # {lang: compendium_filepath}
        self.compendium_files = {}

        # {lang: [msgids]}
        self.compendium_msgids = {}

        # {lang: [msgstrs]}
        self.compendium_msgstrs_tr = {}

        # translations of current page being built
        self.current = None

        # all translations in the build
        # {lang: [Translation(...), Translation(...), ...]}
        self.all = {}

        # possible URL locations of records with its correspondient
        # language, needed to discriminate records on search indexes
        # {location: language}
        self.locations = {}

        # translations statistics for each language
        # {lang: {total: int, translated: int}}
        self.stats = {}

        # config settings translations (site_name, site_description)
        # {lang: {site_name: str, site_description: str}}
        self.config_settings = {}

    def __str__(self):  # pragma: no cover
        current = 'None' if self.current is None else 'Translation(...)'
        return (
            f'Translations(tempdir="{self.tempdir}",'
            f' files={str(self.files)}, nav={str(self.nav)},'
            f' compendium_files={str(self.compendium_files)},'
            f' compendium_msgids={str(self.compendium_msgids)},'
            ' compendium_msgstrs_tr='
            f'{str(self.compendium_msgstrs_tr)},'
            f' current={current},'
            f' locations={str(self.locations)},'
            f' config_settings={str(self.config_settings)}'
            ')'
        )
