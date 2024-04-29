# =====================================
# generator=datazen
# version=3.1.4
# hash=1668f8d26ad800f736638e7eb757119a
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
        "3.10",
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
