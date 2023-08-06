from setuptools import find_packages, setup

setup(
    name="aiobtcrpc",
    packages=find_packages(),
    version="0.1.0",
    description="Asynchronous Bitcoin RPC Client",
    author="@biobdeveloper",
    license="MIT",
    install_requires=["aiohttp==3.7.3"],
    test_suite="tests",
    python_requires=">=3.8"
)
