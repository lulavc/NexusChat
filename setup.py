"""Setup file for nexus_chat package."""
from setuptools import setup, find_packages

setup(
    name="nexus_chat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "customtkinter>=5.2.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.20.0",
    ],
    python_requires=">=3.8",
)
