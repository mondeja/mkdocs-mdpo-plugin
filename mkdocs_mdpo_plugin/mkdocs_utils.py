"""Mkdocs utilities"""

import os

import mkdocs


MKDOCS_MINOR_VERSION_INFO = tuple(
    int(n) for n in mkdocs.__version__.split('.')[:2]
)
LUNR_LANGUAGES_PATH = os.path.join(
    mkdocs.__path__[0], 'contrib', 'search', 'lunr-language',
)


class MkdocsBuild:
    """Represents the Mkdocs build process.

    Is a singleton, so only accepts one build. Should be initialized using
    the `instance` class method, which accepts an instance of the plugin class.
    """
    _instance = None

    @classmethod
    def instance(cls, mdpo_plugin):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.mdpo_plugin = mdpo_plugin
        return cls._instance


def __on_build_error(self):
    self.translations.tempdir.cleanup()
    MkdocsBuild._instance = None


def set_on_build_error_event(MdpoPlugin):
    """mkdocs>=1.2.0 includes a ``build_error`` event executed when the build
    triggers a exception.

    This function patch provides the same cleanup functionality if the
    `build_error` event is not supported.
    """
    if MKDOCS_MINOR_VERSION_INFO >= (1, 2):
        if not hasattr(MdpoPlugin, 'on_build_error'):
            def _on_build_error(self, error):
                return __on_build_error(self)

            MdpoPlugin.on_build_error = _on_build_error
    else:
        import atexit

        def _on_build_error():  # pragma: no cover
            build_instance = MkdocsBuild()
            if hasattr(build_instance, 'mdpo_plugin'):
                return __on_build_error(build_instance.mdpo_plugin)

        atexit.unregister(_on_build_error)
        atexit.register(_on_build_error)


def get_lunr_languages():
    response = []
    for filename in os.listdir(LUNR_LANGUAGES_PATH):
        lang = filename.split('.')[1]
        if len(lang) == 2:
            response.append(lang)
    return response
