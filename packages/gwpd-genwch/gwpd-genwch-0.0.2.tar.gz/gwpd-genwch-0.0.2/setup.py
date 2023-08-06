import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gwpd-genwch",  # Replace with your own username
    version="0.0.2",
    author="genwch",
    author_email="",
    description="Pandas as table package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genwch/gwpd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gwcomm-genwch",
        "Werkzeug==0.16.1",
        "pandas",
        "pyarrow==0.16.0"
    ],
    python_requires='>=3.7',
)
