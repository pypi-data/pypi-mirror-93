from setuptools import setup as setuptools_setup
from setuptools import find_packages as setuptools_find_packages


long_description = '''# Clear Cache
Delete __pycache__ folders in project
# Installing
```
python -m pip install clear_cache
```
# Example
```
from clear_cache import clear as clear_cache
clear_cache()
```'''

setuptools_setup(
    name="clear_cache",
    version="0.0.1",
    author="Pixelsuft",
    description="Delete __pycache__ folders in project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools_find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
    license='MIT', 
    keywords='clear_cache',
    install_requires=[''],
    py_modules=["clear_cache"]
)