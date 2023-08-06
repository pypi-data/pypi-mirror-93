#!/usr/bin/env python

from setuptools import setup

setup(
    name="kropotkin",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "kropotkin/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    packages=["kropotkin"],
    description="Hooks for stateless Django apps",
    install_requires=["msgpack", "hhc"],
)
