import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IPv4Rechner",
    version="1.0",
    author="comiker91",
    author_email="webmaster@nightmaremc.de",
    description="Paket zum Berechnen von IPv4 Adressen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/comiker91",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)