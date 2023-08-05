from setuptools import setup, find_namespace_packages
setup(
    name='omniblack.path',
    version='0.0.2',
    author='Terry Patterson',
    author_email='terryp@wegrok.net',
    license='AGPL-3.0-or-later',
    packages=find_namespace_packages(include=['omniblack.*']),
    zip_safe=False,
    install_requires=(
        'more-itertools',
    ),
)

