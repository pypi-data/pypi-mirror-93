import setuptools

with open("readme.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="au_adsp-mpgriff", # Replace with your own username
    version="0.0.1",
    author="matt griffiths",
    author_email="mpg@ece.au.dk",
    description="A small example package",
    long_description=long_description,
    packages=setuptools.find_packages(),
    url="https://github.com/mpgriff/au_adsp",
    install_requires=['numpy', 'matplotlib', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
