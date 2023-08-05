import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="duckit",
    version="0.0.2",
    author="Kapil Yedidi",
    author_email="kapily.code@gmail.com",
    description="Unofficial DuckDB toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kapily/duckit",
    packages=setuptools.find_packages(),
    install_requires=[
        'dataset>=0.2.3,<1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
