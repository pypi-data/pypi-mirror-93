import setuptools

from version_stamp import version

description = 'Stamping utility'

install_requires=[
    'filelock>=3.0.12',
    'GitPython>=3.1.3',
    'packaging>=3.1.3',
    'PyYAML>=5.3.1',
]

setuptools.setup(
    name='vmn',
    version=version.version,
    author="Pavel Rogovoy",
    author_email='pavelr@final.israel',
    description=description,
    long_description=description,
    python_requires='>=3.5.0',
    url="https://github.com/final-israel/ver_stamp",
    install_requires=install_requires,
    package_dir={'version_stamp': 'version_stamp'},
    packages=['version_stamp',],
    entry_points={
        'console_scripts': ['vmn = version_stamp.vmn:main']
    },
)
