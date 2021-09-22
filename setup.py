import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gtm_gear',
    version='0.0.1',
    author='Artem Korneev',
    author_email='dev.dandp@gmail.com',
    description='Automate everyday Google Tag Manager tasks.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ArtemKorneevGA/gtm-gear',
    project_urls = {
        "Bug Tracker": "https://github.com/ArtemKorneevGA/gtm-gear/issues"
    },
    license='MIT',
    packages=['gtm_gear'],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['ratelimit','google-api-python-client','oauth2client'],
)
