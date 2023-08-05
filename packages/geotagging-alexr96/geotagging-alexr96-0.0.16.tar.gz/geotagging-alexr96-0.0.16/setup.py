import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geotagging-alexr96",
    version="0.0.16",
    author="Alex Roy",
    author_email="Alex@devpipeline.com",
    description="Geotagging database package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-96-devpipeline/geotagging_db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["psycopg2-binary"],
    package_data={
    '': ['*.txt'],
    }
)