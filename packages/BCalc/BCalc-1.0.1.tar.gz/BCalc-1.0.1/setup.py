from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = "BCalc",
  version = "1.0.1",
  description = "A Calculator with many uses",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://modules.breezecodes.com",
  author = "Jace Billingsley",
  author_email = "jacebphotography@outlook.com",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "MIT",
  packages=['MyModule'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)