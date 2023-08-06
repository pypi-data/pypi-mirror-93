"""Pofy installation configuration."""
from pathlib import Path
from re import compile as re_compile
from subprocess import CalledProcessError
from subprocess import DEVNULL
from subprocess import check_output

from setuptools import setup


def get_git_version() -> str:
    """Get package version from git tags."""
    pattern = re_compile(
        r'^v(?P<version>\d*\.\d*\.\d*)(-\d*-g(?P<commit>\d*))?'
    )
    try:
        command = [
            'git', 'describe',
            '--tags',
            '--match', 'v[0-9]*.[0-9]*.[0-9]*'
        ]
        version_bytes = check_output(command, stderr=DEVNULL)
        version = version_bytes.decode('utf-8')
        match = pattern.match(version)
        if match is not None:
            commit = match.group('commit')
            version = match.group('version')
            if commit is not None:
                version = '{}.dev{}'.format(version, commit)
            return version.rstrip()
    except CalledProcessError:
        pass

    return '0.0.0'


setup(
    name="pofy",
    description="Python Yaml Object deserializer based on PyYAML.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    version=get_git_version(),
    keywords=['YAML', 'serialization'],
    packages=[
        'pofy',
        'pofy.fields',
        'pofy.tag_handlers'
    ],
    license='WTFPL',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    install_requires=['pyyaml'],
    author="An Otter World",
    author_email="an-otter-world@ki-dour.org",
    url="http://github.com/an-otter-world/pofy/",
    zip_safe=False,
)
