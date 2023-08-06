from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dsp-metadata-gui",
    version="0.0.0-rc001",
    description="Python GUI tool to collect metadata for DSP projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasch-swiss/dsp-metadata-gui",
    author="Balduin Landolt",
    author_email="balduin.landolt@dasch.swiss",
    license="GPLv3",
    packages=["dspMetadataGUI", "dspMetadataGUI.util"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
    install_requires=[
        "pyshacl==0.14.2",
        "rdflib==5.0.0",
        "rdflib-jsonld==0.5.0",
        "wxPython==4.1.1",
    ],
    entry_points={
        "console_scripts": [
            "dsp-metadata=dspMetadataGUI.collectMetadata:collectMetadata"
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
