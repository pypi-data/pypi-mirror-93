import re
from pathlib import Path

from setuptools import find_packages, setup

version_regex = re.compile(
    r"^__version__\s*=\s*\((?P<major>\d+),\s*(?P<minor>\d+),"
    r"\s*(?P<patch>\d+)"
    r"(?:,\s*(?P<quote>[\"\'])(?P<prerelease>\w+)(?P=quote))?\)$",
)


def find_version():
    version_file = Path("migreat/__init__.py")
    with version_file.open() as fp:
        for line in fp.readlines():
            version_match = version_regex.fullmatch(line.strip())
            if version_match:
                break

    major = version_match.group("major")
    minor = version_match.group("minor")
    patch = version_match.group("patch")
    prerelease = version_match.group("prerelease")

    v = f"{major}.{minor}.{patch}"
    if prerelease:
        v += f"-{prerelease}"
    return v


def find_requires():
    requirements_file = Path("min-requirements.txt")
    with requirements_file.open() as fp:
        return [line.strip() for line in fp.readlines() if line.strip()]


setup(
    name="migreat",
    author="João Sampaio",
    author_email="jpmelos@gmail.com",
    version=find_version(),
    description="A flexible SQL migration runner.",
    long_description=(
        "For more information, visit https://github.com/jpmelos/migreat."
    ),
    long_description_content_type="text/plain",
    keywords=[
        "database",
        "databases",
        "psql",
        "postgresql",
        "postgres",
        "sql",
        "migration",
        "migrations",
    ],
    url="https://github.com/jpmelos/migreat",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database",
    ],
    python_requires=">=3.7,<3.10",
    packages=find_packages(include=["migreat", "migreat.*"]),
    install_requires=find_requires(),
    entry_points={"console_scripts": ["migreat=migreat.__main__:cli"]},
)
