from setuptools import find_packages, setup
from TwitchX import __version__

setup(
    name="TwitchX",
    version=__version__,
    description="Netchive-Lite Twitch Extension",
    url="https://netchive.com/",
    author="Netchive™ Team",
    author_email="contact@netchive.com",
    keywords=[
        "TwitchX", "Twitch", "Netchive", "Extension"
    ],
    install_requires=[
        "aiohttp[speedups]",
        "aiographql-client",
        "pydantic",
        "ujson",
        "user_agent",
        "Scrapy",
        "browser_cookie3",
        "requests"
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Free for non-commercial use",
        "Development Status :: 3 - Alpha"
    ],
    zip_safe=False,
)
