import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qleda",
    version="0.1.3",
    author="René Locher",
    author_email="rene_locher@hotmail.com",
    description="QLEDA is a python project to read or create schematics and netlists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/locher/qleda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'numpy>=1.19.4',
        'pycairo>=1.20.0',
        'SQLAlchemy>=1.3.0'
    ],
)