import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typan",
    version="0.0.7",
    author="BruhDev",
    author_email="mr.bruh.dev@gmail.com",
    description="Extra features for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bruhdev.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)