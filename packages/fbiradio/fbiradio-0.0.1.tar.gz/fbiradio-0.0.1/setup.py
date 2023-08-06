import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fbiradio",
    version="0.0.1",
    author="Christian Christiansen",
    author_email="christian.l.christiansen@gmail.com",
    description="Find currently playing track on FBi Radio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cchristiansen/fbiradio",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    include_package_data=True,
    scripts=['bin/fbiplaying'],
    python_requires=">=3.6",
)
