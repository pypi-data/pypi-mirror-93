import setuptools

REQUIRED = ["numpy", "pandas"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambdata-Vgrams05", 
    version="0.0.1",
    author="Virginia Grams",
    description="A collection of Data Science functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vgrams05/lambdata-Vgrams05.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)