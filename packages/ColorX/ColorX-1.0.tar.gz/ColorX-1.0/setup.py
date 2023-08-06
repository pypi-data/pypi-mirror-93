import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ColorX",
    version="1.0",
    author="Caz",
    description="First Python Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Caz-Developer/colorx",
    packages=setuptools.find_packages(),
    install_requires=["requests", "os", "time"]
)