import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoforecast", # Replace with your own username
    version="0.0.6",
    author="Guillaume Simo",
    author_email="guillaume.simo@hotmail.fr",
    description="AutoML time series forecasting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuillaumeSimo/autoforecast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt', 'r').read().split()
)