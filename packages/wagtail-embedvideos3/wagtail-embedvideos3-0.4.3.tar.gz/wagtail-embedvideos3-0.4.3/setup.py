#!/usr/bin/env python
from distutils.core import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wagtail-embedvideos3',
    version='0.4.3',
    description='Embed Videos for Wagtail CMS.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='InfoPortugal S.A.',
    author_email='suporte24@infoportugal.com',
    maintainer='Romaniuk Oleksandr',
    maintainer_email='oleksandr.romaniuk@protonmail.com',
    url='https://github.com/olksndrdevhub/wagtail-embed-videos3',
    packages=setuptools.find_packages(),
    package_data={
        'wagtail_embed_videos': [
            'static/wagtail_embed_videos/js/*.js',
            'templates/wagtail_embed_videos/chooser/*.html',
            'templates/wagtail_embed_videos/edit_handlers/*.html',
            'templates/wagtail_embed_videos/embed_videos/*.html',
            'templates/wagtail_embed_videos/widgets/*.html',
        ]
    },
    install_requires=[
        'wagtail>=2.0',
        'django-embed-video>=1.4',
        'six>=1.15.0'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License'],
    license='New BSD',

)
