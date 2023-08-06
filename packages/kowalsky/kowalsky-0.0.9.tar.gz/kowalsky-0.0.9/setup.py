import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(
    name="kowalsky",
    version="0.0.9",
    author="Nikita Gordia",
    author_email="nikita.gordia@gmail.com",
    description="A small package for all useful ML things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NikitaGordia/Kowalsky",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=REQUIREMENTS,
    python_requires='>=3.6',
)