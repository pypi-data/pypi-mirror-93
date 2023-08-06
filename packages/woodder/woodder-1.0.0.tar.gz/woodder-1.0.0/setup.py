import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="woodder",
    version="1.0.0",
    description="A really simple logger configurator for Python 3.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ArshanKhanifar/woodder",
    author="Arshan Khanifar",
    author_email="arshankhanifar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["src"],
    include_package_data=False,
    install_requires=[]
)
