import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ch-password-generator",
    version="0.8.2.dev1",
    author="Jakub Pocentek",
    author_email="pocedev@gmail.com",
    description="A simple password generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpocentek/passgen/",
    license_file="LICENSE.txt",
    keywords="password generator",
    packages=setuptools.find_packages(include=["passgen"]),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="~=2.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "passgen=passgen:main",
        ],
    },
)
