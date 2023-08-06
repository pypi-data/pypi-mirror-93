import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portx",
    version="0.0.2",
    author="Neil Lambeth",
    author_email="neil@redrobotics.co.uk",
    description="Python library for the RedRobotics PPX Programmable Port eXpander",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedRobotics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
