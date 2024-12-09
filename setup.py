from setuptools import setup, find_packages

setup(
    name="simple_said",
    version="0.1.0",
    description="Basic Saidify per KERI specs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dane Ogden",
    author_email="DaneOgden1@gmail.com",
    url="https://github.com/dane-git/simple-said",  
    license="MIT",  
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "blake3==0.4.1",
        "setuptools==75.1.0",
        "wheel==0.44.0"
    ],
    entry_points={
        "console_scripts": [
            "your-cli=simple_said.main:main",  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",  
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)