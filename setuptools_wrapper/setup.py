"""
A simpler setuptools-based package definition.
"""

# built-in
from contextlib import contextmanager
import os
import shutil
from sys import platform, version_info
import tempfile
from typing import Any, Dict, Iterator, List, Set, Union, cast

# third-party
import setuptools

SELF = "setuptools-wrapper"


@contextmanager
def inject_self(
    working_dir: str,
    curr_pkg_slug: str,
    pkg: str = SELF,
    force_copy: bool = False,
) -> Iterator[None]:
    """
    Copy this entire package into the caller's source distribution. This is
    the only way to avoid a pointless requirement to already have this package
    installed to install anything else, and also generally not requiring
    an explicit install of this package except for command-line use.
    """

    added = False
    pkg = pkg.replace("-", "_")

    # inject sources into a package with a different name, otherwise
    # installation becomes very broken and messed up
    to_create = os.path.join(working_dir, f"{curr_pkg_slug}_bootstrap")

    try:
        # do nothing if we are building ourselves (but allow forcing this)
        if (force_copy or pkg not in curr_pkg_slug) and not os.path.isdir(
            to_create
        ):
            os.mkdir(to_create)

            # copy our sources into their package
            to_copy = [
                "__init__.py",
                "setup.py",
                "py.typed",
            ]
            vmklib_dir = os.path.dirname(__file__)
            for fname in to_copy:
                dest = os.path.join(to_create, fname)
                src = os.path.join(vmklib_dir, fname)
                if not os.path.isfile(dest) and os.path.isfile(src):
                    shutil.copyfile(src, dest)

            added = True

        yield
    finally:
        if added:
            shutil.rmtree(to_create)


def get_long_description(desc_filename: str = "README.md") -> str:
    """Get a package's long-description data from a file."""

    try:
        with open(desc_filename, "r", encoding="utf-8") as desc_file:
            long_description = desc_file.read()
        return long_description
    except FileNotFoundError:
        return ""


def default_requirements_file(directory: str) -> str:
    """Default location to look for the requirements file."""

    return os.path.join(directory, "requirements.txt")


def get_requirements(reqs_filename: str) -> Set[str]:
    """Get a package's requirements based on its requirements file."""

    try:
        with open(reqs_filename, "r", encoding="utf-8") as reqs_file:
            return set(x.strip() for x in reqs_file)
    except FileNotFoundError:
        return set()


def get_data_files(pkg_name: str, data_dir: str = "data") -> List[str]:
    """
    Get the non-code sources under a package directory's data directory.
    """

    data_files = []
    for root, _, files in os.walk(os.path.join(pkg_name, data_dir)):
        for fname in files:
            rel_name = os.path.join(root, fname).replace(pkg_name + os.sep, "")
            data_files.append(rel_name)

    return data_files


class PythonVersionCompare:
    """Python version string comparison object."""

    def __init__(
        self, major: int = None, minor: int = None, micro: int = None
    ) -> None:
        """Initialize this instance."""

        if major is None:
            major = version_info.major
        if minor is None:
            minor = version_info.minor
        if micro is None:
            micro = version_info.micro

        self.major = major
        self.minor = minor
        self.micro = micro

    @staticmethod
    def from_str(data: str) -> "PythonVersionCompare":
        """Create a version comparison instance from a string."""

        parts = data.strip().split(".")

        major = None
        minor = None
        micro = None

        for part in parts:
            as_int = int(part)

            if major is None:
                major = as_int
            elif minor is None:
                minor = as_int
            elif micro is None:
                micro = as_int

        return PythonVersionCompare(major=major, minor=minor, micro=micro)

    def cmp(self, other) -> int:
        """Compare to an object."""

        if isinstance(other, str):
            other = PythonVersionCompare.from_str(other)

        assert isinstance(other, PythonVersionCompare)

        diff = self.major - other.major
        if diff != 0:
            return diff

        diff = self.minor - other.minor
        if diff != 0:
            return diff

        return self.micro - other.micro

    def __lt__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) < 0

    def __le__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) <= 0

    def __eq__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) == 0

    def __ne__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) != 0

    def __gt__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) > 0

    def __ge__(self, other) -> bool:
        """Compare to an object."""
        return self.cmp(other) >= 0


def process_requirements(requirements: Set[str]) -> Set[str]:
    """Process conditional statements in requirement declarations."""

    new_reqs: Set[str] = set()

    for requirement in requirements:
        parts = [x.strip() for x in requirement.split(";")]
        if len(parts) == 1:
            new_reqs.add(parts[0])
        elif eval(  # pylint: disable=eval-used
            parts[1],
            {},
            {
                "sys_platform": platform,
                "python_version": PythonVersionCompare(),
            },
        ):
            new_reqs.add(parts[0])

    return new_reqs


# pylint: disable=too-many-arguments
def setup(
    pkg_info: Dict[str, Any],
    author_info: Dict[str, str],
    url_override: str = None,
    classifiers_override: List[str] = None,
    requirements: Set[str] = None,
    **kwargs,
) -> None:
    """
    Build a 'setuptools.setup' call with sane defaults and making assumptions
    about certain aspects of a package's structure.
    """

    defaults: Dict[str, Union[str, List[str], Set[str]]] = {
        "url_override": (
            f"https://github.com/{author_info['username']}/"
            f"{pkg_info['name']}"
        ),
        "classifiers_override": [
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        "requirements": set(),
    }

    # Resolve defaults if necessary.
    url_override = cast(
        str, defaults["url_override"] if url_override is None else url_override
    )
    classifiers_override = cast(
        List[str],
        defaults["classifiers_override"]
        if classifiers_override is None
        else classifiers_override,
    )
    requirements = cast(
        Set[str],
        defaults["requirements"] if requirements is None else requirements,
    )

    for version in pkg_info.get("versions", []):
        classifiers_override.append(
            f"Programming Language :: Python :: {version}"
        )

    # Find requirements files inside the package's root directory.
    req_files = [default_requirements_file(pkg_info["slug"])]
    for req_file in req_files:
        requirements |= get_requirements(req_file)

    with tempfile.TemporaryDirectory() as temp_dir:
        working_dir = temp_dir
        dir_contents = os.listdir(os.getcwd())
        if pkg_info["slug"] in dir_contents:
            working_dir = os.getcwd()

        with inject_self(
            working_dir,
            pkg_info["slug"],
            force_copy=pkg_info.get("force_copy", False),
        ):
            setuptools.setup(
                name=pkg_info["name"],
                version=pkg_info["version"],
                author=author_info["name"],
                author_email=author_info["email"],
                description=pkg_info["description"],
                long_description=get_long_description(),
                long_description_content_type="text/markdown",
                url=url_override,
                packages=setuptools.find_namespace_packages(
                    include=[pkg_info["slug"], pkg_info["slug"] + ".*"],
                    exclude=["tests", "tests.*"],
                ),
                classifiers=classifiers_override,
                python_requires=f">={pkg_info.get('versions', ['3.6'])[0]}",
                install_requires=list(process_requirements(requirements)),
                package_data={
                    pkg_info["slug"]: (
                        get_data_files(pkg_info["slug"])
                        + ["py.typed", "*.pyi", "*.txt"]
                    ),
                    f"{pkg_info['slug']}_bootstrap": ["py.typed"],
                    "": ["*.pyi"],
                },
                **kwargs,
            )
