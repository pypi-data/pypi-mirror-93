import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_youtube",
    version="1.0.3",
    author="Kovács Kristóf-Attila & Péntek Zsolt",
    description="selenium_youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_youtube",
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'kcu',
        'kstopit',
        'kyoutubescraper',
        'selenium',
        'selenium-firefox',
        'selenium-uploader-account'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)