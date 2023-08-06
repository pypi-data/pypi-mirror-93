import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beeth0ven_internal_python_graphql_client", 
    version="0.0.2",
    author="Luo Jie",
    author_email="beeth0vendev@gmail.com",
    description="It's a simple graphQL client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.picroup.com:444/beeth0ven/beeth0ven_internal_python_graphql_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-graphql-client>=0,<1',
    ],
    python_requires='>=3.6',
)