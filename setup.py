# =====================================
# generator=datazen
# version=3.1.2
# hash=8a67dab69591ed0cc9d0607e9d700a56
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
        "3.8",
        "3.9",
        "3.10",
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
