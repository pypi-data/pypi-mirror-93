import setuptools

with open("README.md") as f:
    long_desc = f.read()

setuptools.setup(
        name="asen_6008",
        version="1.0.0",
        author="Nickolai Belakovski",
        description="Constants for CU Boulder's ASEN 6008",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/nbelakovski/asen_6008",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free For Educational Use",
        "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        )
