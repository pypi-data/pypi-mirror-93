from setuptools import setup

setup(
    name = 'planetfilter',
    version = '0.10.0',
    description = 'Filter for blog aggregators',
    author = 'Francois Marier',
    author_email = 'francois@fmarier.org',
    url = 'https://launchpad.net/planetfilter',
    scripts = ['planetfilter'],
    keywords = ['rss', 'atom', 'blogs', 'planet'],
    license = 'AGPL-3.0+',
    requires = ['defusedxml'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        ],
    long_description_content_type = 'text/x-rst',
    long_description = """\
PlanetFilter uses a user-provided filter to prune blog aggregator
feeds. It allows anyone to subscribe to popular blog aggregators
without being overwhelmed by the noise.

.. _project page: https://launchpad.net/planetfilter
"""
    )
