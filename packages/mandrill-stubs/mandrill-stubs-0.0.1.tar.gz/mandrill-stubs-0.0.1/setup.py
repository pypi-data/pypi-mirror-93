import os.path

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, "", 1)
            stubs.append(path)
    return {package: stubs}

setuptools.setup(
    name="mandrill-stubs",
    version="0.0.1",
    author="Tim Martin",
    author_email="tim@asymptotic.co.uk",
    description="Type declarations for the Mandrill API",
    url="https://github.com/timmartin/mandrill-stubs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['mandrill-stubs'],
    install_requires=[
        "mandrill>=1.0.59"
    ],
    package_data=find_stubs("mandrill-stubs"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed"
    ],
    zip_safe=False
)
