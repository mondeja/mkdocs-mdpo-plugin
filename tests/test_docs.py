"""Specific tests for the own documentation of mkdocs-mdpo-plugin."""

import os
import re

from mdpo import __version__ as __mdpo_version__
from pre_commit_po_hooks import __version__ as __pre_commit_po_hooks_version__


DOCS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'docs',
)


def test_useful_recipes_precommit_hooks_versions():
    """pre-commit hooks versions of examples at Useful recipes page
    must be in the last version.
    """
    useful_recipes_path = os.path.join(DOCS_DIR, 'src', 'useful-recipes.md')

    with open(useful_recipes_path) as f:
        content_lines = f.readlines()

    versions = {
        'po_hooks': None,
        'mdpo': None,
    }
    for i, line in enumerate(content_lines):
        if 'repo:' in line:
            if 'https://github.com/mondeja/pre-commit-po-hooks' in line:
                match = re.search(
                    r'v(\d+\.\d+\.\d+)',
                    content_lines[i + 1],
                )
                if match:
                    versions['po_hooks'] = match.group(1)
            elif 'https://github.com/mondeja/mdpo' in line:
                match = re.search(
                    r'v(\d+\.\d+\.\d+)',
                    content_lines[i + 1],
                )
                if match:
                    versions['mdpo'] = match.group(1)

    assert __pre_commit_po_hooks_version__ == versions['po_hooks'], (
        f'Version v{versions["po_hooks"]} of pre-commit-po-hooks configuration'
        f' must be updated to v{__pre_commit_po_hooks_version__} in file'
        f' {useful_recipes_path}'
    )

    assert __mdpo_version__ == versions['mdpo'], (
        f'Version v{versions["po_hooks"]} of mdpo pre-commit hook'
        f' configuration must be updated to v{__mdpo_version__} in file'
        f' {useful_recipes_path}'
    )
