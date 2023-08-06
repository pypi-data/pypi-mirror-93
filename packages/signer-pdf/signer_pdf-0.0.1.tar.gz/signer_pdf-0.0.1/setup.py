import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signer_pdf",
    version="0.0.1",
    author="Roman Grigoriev",
    author_email="hjklvfr@list.ru",
    description="A signer pdf with image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Hjklvfr/signer_pdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
