from setuptools import setup
import os

VERSION = "0.2.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-leaflet",
    description="A plugin that bundles Leaflet.js for Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-leaflet",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-leaflet/issues",
        "CI": "https://github.com/simonw/datasette-leaflet/actions",
        "Changelog": "https://github.com/simonw/datasette-leaflet/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_leaflet"],
    entry_points={"datasette": ["leaflet = datasette_leaflet"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-leaflet[test]"],
    package_data={
        "datasette_leaflet": [
            "static/*.js",
            "static/*.css",
            "static/images/*",
        ],
    },
    python_requires=">=3.6",
)
