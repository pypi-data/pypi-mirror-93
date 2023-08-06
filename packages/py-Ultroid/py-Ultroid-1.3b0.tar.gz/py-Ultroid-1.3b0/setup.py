import setuptools

REQUIREMENTS = "requirements.txt"
req = open(REQUIREMENTS, "r")
z = req.read()
req.close()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "py-Ultroid"
version = "1.3-beta"
author = "TeamUltroid"
author_email = "teamultroid@protonmail.ch"
description = "#todo"
install_requires = z.split("\n")
url = "https://github.com/TeamUltroid/Ultroid"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
