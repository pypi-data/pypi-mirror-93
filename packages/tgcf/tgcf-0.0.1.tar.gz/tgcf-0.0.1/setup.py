from setuptools import setup, find_packages
import pathlib
import re

here = pathlib.Path(__file__).parent.resolve()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('tgcf/__init__.py', 'r').read(),
    re.M).group(1)

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='tgcf',
    version=version,
    description='A simple script to forward all the messages of one chat (indivisual/group/channel) to another. Made using Telethon. Can be used for backup or cloning.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aahnik/telegram-chat-forward',
    author='Aahnik Daw',
    author_email='meet.aahnik@gmail.com',

    classifiers=[

        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='telegram,bot,forwarder,script,backup,clone,telegram userbot,telethon',

    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['Telethon', 'python-dotenv', 'typer'],

    entry_points={
        'console_scripts': [
            'tgcf=tgcf:cli.app',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/aahnik/telegram-chat-forward/issues',
        'Funding': 'https://telegram.me/aahnikdaw',
        'Say Thanks!': 'https://telegram.me/aahnikdaw',
        'Source': 'https://github.com/aahnik/telegram-chat-forward',
        'Forum': 'https://github.com/aahnik/telegram-chat-forward/discussions'
    },
)
