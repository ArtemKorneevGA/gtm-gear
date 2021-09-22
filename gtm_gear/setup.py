import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="gtm-gear",
    version="0.1",
    scripts=["gtm-gear"],
    author="Artem Korneev",
    author_email="dev.dandp@gmail.com",
    description="GTM API automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArtemKorneevGA/gtm-gear",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

