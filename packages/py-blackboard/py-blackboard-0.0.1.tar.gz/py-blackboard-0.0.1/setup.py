import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-blackboard",
    version="0.0.1",
    author="Paolo Rollo",
    author_email="paolo.rollo1997@gmail.com",
    description="Python library to interact with the Blackboard Collaborate APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PaoloRollo/py-blackboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)