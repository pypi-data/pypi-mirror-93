import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YUM - menu tree", # Replace with your own username
    version="0.0.1",
    author="Bashir Filipp",
    author_email="filipp218@gmail.com",
    description="menu tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipp218/test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
