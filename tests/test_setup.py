"""
Test the 'setup' module.
"""

# built-in
import os
from sys import platform
import tempfile

# third-party
import setuptools

# module under test
from setuptools_wrapper import DESCRIPTION, PKG_NAME, VERSION
from setuptools_wrapper.setup import process_requirements
from setuptools_wrapper.setup import setup as setup_fn


def test_process_requirements():
    """Test the 'process_requirements' method."""

    assert process_requirements(
        {"test", f"test2; sys_platform == '{platform}'"}
    ) == {"test", "test2"}


def test_setup_fn():
    """
    Test that that package-building capability we expose externally works.
    """

    author_info = {
        "name": "Example Example",
        "email": "Example@example.com",
        "username": "example",
    }
    pkg_info = {
        "name": PKG_NAME,
        "version": VERSION,
        "description": DESCRIPTION,
        "versions": ["3"],
        "force_copy": True,
    }
    pkg_info["slug"] = str(pkg_info["name"]).replace("-", "_")

    def setup_stub(*_, **__):
        """Don't do anything."""

    real_setup = setuptools.setup
    setuptools.setup = setup_stub

    start_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as temp_dir:
        setup_fn(pkg_info, author_info, entry_override="mk")
        setup_fn(pkg_info, author_info)
        os.chdir(temp_dir)
        setup_fn(pkg_info, author_info)
        os.chdir(start_dir)

    setuptools.setup = real_setup
