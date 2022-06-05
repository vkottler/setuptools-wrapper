# =====================================
# generator=datazen
# version=2.1.0
# hash=1648a85b1a4aface73daaa0a4b76d934
# =====================================

"""
setuptools-wrapper - Package definition for distribution.
"""

# internal
from setuptools_wrapper import DESCRIPTION, PKG_NAME, VERSION

try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from setuptools_wrapper_bootstrap.setup import setup  # type: ignore

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.7",
        "3.8",
        "3.9",
        "3.10",
    ],
}
setup(
    pkg_info,
    author_info,
)
