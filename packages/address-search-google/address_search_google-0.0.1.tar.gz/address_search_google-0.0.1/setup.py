import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="address_search_google",
    version="0.0.1",
    author="Saurabh Pandey",
    author_email="scoder91@gmail.com",
    description="Google Search API with Caching for repeated search.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dextrop/address_search_google",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)