from setuptools import setup

package = "flake8-safegraph-crawl"
version = "0.1"

setup(
    name=package,
    version=version,
    description="Flake8 plugin with linting checks for SafeGraph crawlers",
    url="https://github.com/SafeGraphInc/flake8-safegraph-crawl",
    packages=["flake8_safegraph_crawl"],
    entry_points={"flake8.extension": ["SG = flake8_safegraph_crawl:Plugin"]},
)
