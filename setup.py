import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fpl_client",
    version="0.1.1",
    author="hiracky16",
    author_email="h.piiice16@gmail.com",
    description="Can get Fantasy Premier League information by using this modules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hiracky16/fpl_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
