import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gwcomm-genwch",  # Replace with your own username
    version="0.0.4",
    author="genwch",
    author_email="",
    description="Common functions package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genwch/gwcomm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
