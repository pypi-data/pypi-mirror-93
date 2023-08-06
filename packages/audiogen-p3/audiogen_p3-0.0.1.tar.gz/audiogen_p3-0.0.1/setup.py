#!/usr/bin/env python

from setuptools import setup, find_packages
import pathlib

required_modules = []
extras_require = {
	'soundcard_playback': ['pyaudio'],
}

here				= pathlib.Path(__file__).parent.resolve()
long_description	= ( here / 'README.rst' ).read_text( encoding='utf-8' )

setup(
	name="audiogen_p3",
	version="0.0.1",
	description="Generator based tools for working with audio clips.",
	author="Ryan Guisewite",
	author_email="ryan.guisewite@gmail.com",
	url="https://github.com/rguisewite/audiogen_p3",

	packages=find_packages(exclude='tests'),
	install_requires=required_modules,
	extras_require=extras_require,

	tests_require=["nose"],
	test_suite="nose.collector",

	long_description=long_description,
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python :: 3.9",
		"Intended Audience :: Developers",
		"Topic :: Multimedia :: Sound/Audio",
	],
    python_requires='>=3.6',
)

