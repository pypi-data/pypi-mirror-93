import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hiven.py",
    version="0.0.1",
    author="teamcodebyte",
    author_email="trustedmercury@gmail.com",
    description="An opensource API wrapper for the Hiven API!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamcodebyte/hiven.py",
    keywords="api, api wrapper, hiven, bot",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
