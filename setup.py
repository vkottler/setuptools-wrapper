# =====================================
# generator=datazen
# version=2.1.0
# hash=11bd4b89c5429fa044e4befcfc132263
# =====================================

"""
setuptools-wrapper - Package definition for distribution.
"""

# third-party
try:
    from vmklib.setup import setup
except (ImportError, ModuleNotFoundError):
    from setuptools_wrapper_bootstrap.setup import setup  # type: ignore

# internal
from setuptools_wrapper import DESCRIPTION, PKG_NAME, VERSION

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
        "3.6",
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
