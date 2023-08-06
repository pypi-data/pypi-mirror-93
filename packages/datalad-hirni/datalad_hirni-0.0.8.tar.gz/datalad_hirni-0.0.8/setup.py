#!/usr/bin/env python

import os.path as op
from setuptools import (
    setup,
    find_packages,
    findall
)

from setup_support import (
    BuildManPage,
    get_version
)


# extension version
version = get_version()

cmdclass = {
    'build_manpage': BuildManPage,
    #'build_examples': BuildRSTExamplesFromScripts,
}


# PyPI doesn't render markdown yet. Workaround for a sane appearance
# https://github.com/pypa/pypi-legacy/issues/148#issuecomment-227757822
README = op.join(op.dirname(__file__), 'README.md')
try:
    import pypandoc
    long_description = pypandoc.convert(README, 'rst')
except (ImportError, OSError) as exc:
    # attempting to install pandoc via brew on OSX currently hangs and
    # pypandoc imports but throws OSError demanding pandoc
    print(
        "WARNING: pypandoc failed to import or thrown an error while converting"
        " README.md to RST: %r   .md version will be used as is" % exc
    )
    long_description = open(README).read()


def findsome(subdir, extensions):
    """Find files under subdir having specified extensions
    Leading directory (datalad) gets stripped
    """
    return [
        f.split(op.sep, 1)[1] for f in findall(op.join('datalad_hirni', subdir))
        if op.splitext(f)[-1].lstrip('.') in extensions
    ]


setup(
    # basic project properties can be set arbitrarily
    name="datalad_hirni",
    author="DataLad developers",
    author_email="team@datalad.org",
    version=version,
    description="DataLad extension for raw data capturing and "
                "conversion workflows",
    long_description=long_description,
    packages=[pkg for pkg in find_packages('.') if pkg.startswith('datalad')],
    zip_safe=False,
    # datalad command suite specs from here
    install_requires=[
        'datalad[full]>=0.14.0',
        'datalad-metalad>=0.2.0',
        'datalad-neuroimaging>=0.3.1',
        'datalad-container>=1.1.2',
        'datalad-webapp>=0.3',
    ],
    extras_require={
        'devel-docs': [
            # used for converting README.md -> .rst for long_description
            'pypandoc',
            # Documentation
            'sphinx>=1.6.2',
            'sphinx-rtd-theme',
        ]},
    cmdclass=cmdclass,
    package_data={
        'datalad_hirni': findsome('resources',
                                  {'sh', 'html', 'js', 'css', 'png', 'svg',
                                   'txt', 'py'})
    },
    entry_points={
        'datalad.extensions': [
            # the label in front of '=' is the command suite label
            # the entrypoint can point to any symbol of any name, as long it is
            # valid datalad interface specification (see demo in this extensions
            'hirni=datalad_hirni:command_suite',
        ],
        'datalad.webapp.apps': [
            'hirni=datalad_hirni:webapp_location',
        ],
        'datalad.tests': [
            'hirni=datalad_hirni',
        ],
    },
    include_package_data=True,
)
