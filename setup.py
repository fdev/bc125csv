from setuptools import setup

description = (
    "Channel import and export tool for the BC125AT, UBC125XLT and UBC126AT."
)
try:
    # Convert from Markdown to reStructuredText (supported by PyPi).
    import os
    import pypandoc

    readme = os.path.join(os.path.dirname(__file__), "README.md")
    long_description = pypandoc.convert(readme, "rst")
except ImportError:
    long_description = description

setup(
    name="bc125csv",
    version="1.1.0",
    url="http://github.com/fdev/bc125csv/",
    download_url="http://github.com/fdev/bc125csv/tarball/master",
    license="MIT",
    description=description,
    long_description=long_description,
    author="Folkert de Vries",
    author_email="bc125csv@fdev.nl",
    packages=["bc125csv"],
    # pySerial list_ports returns ListPortInfo instead of tuple since 3.0.
    install_requires=["pyserial>=3"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["bc125csv=bc125csv:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Communications :: Ham Radio",
    ],
)
