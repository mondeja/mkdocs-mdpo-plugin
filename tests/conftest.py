"""Configuration for mkdocs_mdpo_plugin tests."""

import os
import sys


ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
