import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantnn",
    version="0.0.1dev",
    author="Simon Pfreundschuh",
    description="Quantile regression neural networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonpf/quantnn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "scipy", "paramiko", "einops"],
    python_requires=">=3.6",
)
