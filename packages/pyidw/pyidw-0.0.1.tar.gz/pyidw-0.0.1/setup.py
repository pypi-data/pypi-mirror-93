import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyidw", # Replace with your own username
    version="0.0.1",
    author="Md. Yahya Tamim",
    author_email="yahyatamim0@gmail.com",
    description="A python package intended to impliment GIS like IDW interpolation in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license = 'MIT',
    install_requires = ['geopandas','rasterio'],
    keywords = 'IDW interpolation'
)
