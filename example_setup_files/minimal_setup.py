from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="py_template",
    description="Template Python repository",    
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=("LICENSE.rst",),
    author="Jeff Jennings",
    author_email="jjennings@flatironinstitute.org",
    packages=find_packages(),    
    python_requires=">=3.10",
    install_requires=["numpy >= 1.24"],
)