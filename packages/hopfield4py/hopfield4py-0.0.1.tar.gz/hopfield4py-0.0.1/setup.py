import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hopfield4py",
    version="0.0.1",
    author="Filippo Valle",
    author_email="filippo.valle@unito.it",
    description="Package to run Hopfield model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/fvalle01/hopfield4py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["tensorflow"],
    python_requires='>=3.6',
)
