from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = "EzCalc",
  version = "1.0.0",
  description = "A Basic Calculator With Many Functions",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/jacebillingsley",
  author = "Jace Billingsley",
  author_email = "jacebphotography@Outlook.com",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "MIT License",
  packages=['module'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)