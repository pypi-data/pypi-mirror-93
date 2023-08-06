import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mxmul_pkg_ZXW",
    version="0.1.0",
    author="Xiongwen Zheng",
    author_email="1213904351@qq.com",
    description="An example for teaching how to publish a Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)