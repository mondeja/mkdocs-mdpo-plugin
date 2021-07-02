"""Tests for Mkdocs utilities of mkdocs-mdpo-plugin."""

import importlib
import os
import tempfile
import uuid

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
    # patch plugin instance
    file_to_remove = os.path.join(
        tempfile.gettempdir(),
        f'mkdocs-mdpo-plugin--{uuid.uuid4().hex[:8]}.txt',
    )
    unexistent_file = os.path.join(
        tempfile.gettempdir(),
        f'mkdocs-mdpo-plugin--{uuid.uuid4().hex[:8]}.txt',
    )
    with open(file_to_remove, 'w') as f:
        f.write('foo\n')

    class MkdocsFakeMdpoPlugin:
        def __init__(self):
            self._temp_pages_to_remove = [file_to_remove, unexistent_file]

    try:
        plugin = MkdocsFakeMdpoPlugin()

        module = importlib.import_module('mkdocs_mdpo_plugin.mkdocs_utils')
        module.MKDOCS_MINOR_VERSION_INFO = mkdocs_minor_version_info
        module.MkdocsBuild.instance(plugin)
        module.set_on_build_error_event(plugin)

        assert os.path.isfile(file_to_remove)
        assert not os.path.isfile(unexistent_file)

        if mkdocs_minor_version_info >= (1, 2):
            plugin.on_build_error(plugin, 'foo')

            assert not os.path.isfile(file_to_remove)
            assert not os.path.isfile(unexistent_file)
    finally:
        module.MkdocsBuild._instance = None
