import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vexilla_client",
    version="0.0.1",
    author="cmgriffing",
    author_email="cmgriffing@gmail.com",
    description="A client for the Vexilla feature flag system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vexilla/client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)