import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="buddhhu", # Replace with your own username
    version="1.0",
    author="Amit Sharma",
    author_email="amitsharma123234@gmail.com",
    description="A small example package",
    long_description="None",
    long_description_content_type="text/markdown",
    url="https://github.com/buddhhu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)