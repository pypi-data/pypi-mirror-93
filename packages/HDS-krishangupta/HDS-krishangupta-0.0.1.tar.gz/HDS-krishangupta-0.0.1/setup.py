import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HDS-krishangupta", # Replace with your own username
    version="0.0.1",
    author="Krishan Gupta, Debarka Sengupta",
    author_email="krishang@iiitd.ac.in",
    description="Decline in transcriptional homeostasis defines aging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krishan57gupta/HDS",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
