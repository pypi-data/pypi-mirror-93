import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Venue Mapper",
    version="1.0.1",
    author="Laurens Versluis",
    author_email="l.f.d.versluis@vu.nl",
    description="Maps BibTex venue/journal/booktitle strings to their acronyms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atlarge-research/venue_mappings",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
