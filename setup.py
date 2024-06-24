import io
from setuptools import setup, find_packages


# Read in the README for the long description on PyPI
def long_description():
    with io.open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    return readme

def load_config():
    with io.open("spb_label/sdk_config.py") as fid:
        result = {}
        for line in fid:
            try:
                line.index("End of read")
            except:
                splitted_line = line.strip().split("=")
                result[splitted_line[0]] = splitted_line[-1][1:-1]
            else:
                return result

configs = load_config()
setup(
    name=configs.get("SDK_NAME", ""),
    version=configs.get("SDK_VERSION", ""),
    url=configs.get("SDK_URL", ""),
    license=configs.get("SDK_LICENSE", ""),
    author=configs.get("SDK_AUTHOR", ""),
    author_email=configs.get("SDK_AUTHOR_EMAIL", ""),
    description=configs.get("SDK_DESCRIPTION", ""),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "semver",
        "phy-credit==0.9.0",
        "configparser",
    ],
    zip_safe=False,
    dependency_links=[],
)
