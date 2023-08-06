import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(here, 'README.md')) as f:
        return f.read()


# Return version from the package's __version__.py module.
def version():
    about = {}
    with open(os.path.join(here, 'satorix_django', '__version__.py')) as f:
        exec(f.read(), about)
        return about['__version__']


setup(
    name="satorix-django",
    version=version(),
    description="Configure Django application for Satorix environment",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/satorix/satorix-django",
    author="Satorix",
    author_email="tech@satorix.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["satorix_django"],
    include_package_data=True,
    install_requires=[
        "django>=2.2.11",
        "django-heroku",
    ],
    setup_requires=['wheel'],
    test_suite='nose2.collector.collector',
    tests_require=[
        'nose2',
        'testfixtures',
    ],
    entry_points={
        "console_scripts": [
            "satorix-django-config=satorix_django.__main__:main",
        ]
    },
)
