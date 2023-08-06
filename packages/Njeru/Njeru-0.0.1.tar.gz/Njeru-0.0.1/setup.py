import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Njeru", # Replace with your own username
    version="0.0.1",
    author="Njeru",
    author_email="njerudenis0@gmail.com",
    description="To use for my projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Denisnjeru/EHD.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.*',
)