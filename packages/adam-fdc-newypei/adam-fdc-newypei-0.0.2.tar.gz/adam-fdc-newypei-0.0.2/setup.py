import setuptools
from distutils.core import Extension

from Cython.Build import cythonize

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ext_modules = [
    Extension("add_wrapper",
              sources=["addlib/add_wrapper.pyx"],
              extra_objects=['addlib/libadd.a']
              )
]

setuptools.setup(
    name="adam-fdc-newypei",  # Replace with your own username
    version="0.0.2",
    author="Yipei Niu",
    author_email="newypei@gmail.com",
    description="A python package for FDC",
    ext_modules=cythonize(ext_modules),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://newypei.github.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
