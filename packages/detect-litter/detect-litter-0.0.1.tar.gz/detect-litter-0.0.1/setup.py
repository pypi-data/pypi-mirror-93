import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="detect-litter",
    version="0.0.1",
    author="Thibaut Vuillemin",
    author_email="contact@thibautvuillemin.com",
    description="Detect Git Litter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tvuillemin/detect-litter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "detect-litter=detect_litter:main",
        ],
    },
)
