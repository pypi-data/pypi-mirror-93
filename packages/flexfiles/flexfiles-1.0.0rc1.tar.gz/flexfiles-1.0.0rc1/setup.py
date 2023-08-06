import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flexfiles", # Replace with your own username
    version="1.0.0-rc1",
    author="Sven Flake",
    author_email="sven.flake@optano.com",
    description="A convenience package to handle CSV files easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/optano/flexfiles",
    packages=setuptools.find_packages(exclude=["tests", "test_assets"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "flexlog"
    ],
    python_requires='>=3.6',
)