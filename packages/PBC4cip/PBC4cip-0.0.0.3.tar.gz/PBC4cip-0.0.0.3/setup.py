import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PBC4cip",
    version="0.0.0.3",
    author="Ernesto Ramírez-Sáyago, Miguel Angel Medina-Pérez, Octavio Loyola-González",
    author_email="A00513925@itesm.mx, migue@tec.mx, octavioloyola@tec.mx",
    description="PBC4cip classifier for class imbalance problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octavioloyola/PBC4cip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
