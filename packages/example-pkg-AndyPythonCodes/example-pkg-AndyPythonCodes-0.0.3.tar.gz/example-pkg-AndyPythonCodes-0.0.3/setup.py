import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-AndyPythonCodes", # Replace with your own username
    version="0.0.3",
    author="Andy Arciniega",
    author_email="servidorandycode@gmail.com",
    description="send pdf to server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndyPythonCode/Cliente-Servidor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['django',]
)