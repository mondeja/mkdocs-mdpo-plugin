"""Tests for Mkdocs utilities of mkdocs-mdpo-plugin."""

import importlib
import os
import tempfile

import pytest


@pytest.mark.parametrize(
    'mkdocs_minor_version_info',
    (
        pytest.param(
            (1, 1),
            id='mkdocs_minor_version_info=1.1.2',
        ),
        pytest.param(
            (1, 2),
            id='mkdocs_minor_version_info=1.2.1',
        ),
    ),
)
def test_set_on_build_error_event(mkdocs_minor_version_info):
    class FakeTranslations:
        def __init__(self):
            self.tempdir = tempfile.TemporaryDirectory(
                prefix='mkdocs_mdpo__test_set_on_build_error_event',
            )

    class MkdocsFakeMdpoPlugin:
        def __init__(self):
            self.translations = FakeTranslations()

    try:
        plugin = MkdocsFakeMdpoPlugin()

        module = importlib.import_module('mkdocs_mdpo_plugin.mkdocs_utils')
        module.MKDOCS_MINOR_VERSION_INFO = mkdocs_minor_version_info
        module.MkdocsBuild.instance(plugin)
        module.set_on_build_error_event(plugin)

        assert os.path.isdir(plugin.translations.tempdir.name)

        if mkdocs_minor_version_info >= (1, 2):
            plugin.on_build_error(plugin, 'foo')

            assert not os.path.isdir(plugin.translations.tempdir.name)
    finally:
        module.MkdocsBuild._instance = None
