import os
import shutil
import subprocess
import sys

import pytest


EXAMPLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'examples',
)


@pytest.mark.parametrize('example_dirname', os.listdir(EXAMPLES_DIR))
def test_examples(example_dirname):
    example_dirpath = os.path.join(EXAMPLES_DIR, example_dirname)
    site_dir = os.path.join(example_dirpath, 'site')
    if os.path.isdir(site_dir):
        shutil.rmtree(site_dir)

    proc = subprocess.run(
        [sys.executable, '-m', 'mkdocs', 'build'],
        cwd=example_dirpath,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    norm_stderr = proc.stderr.decode('utf-8').lower()
    assert proc.returncode == 0
    assert 'warning' not in norm_stderr
    assert 'error' not in norm_stderr

    assert os.path.isdir(site_dir)
