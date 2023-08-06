from setuptools import setup, find_packages


long_description = '''# Clear Cache
Remove __pycache__ folder
# Installation
```
python -m pip install clear_cache
```
# Example
```
from clear_cache import clear as clear_cache
clear_cache(dir = ".")
```
'''

setup(
    name="clear_cache",
    version="1.0.0",
    author="Pixelsuft",
    description="Remove __pycache__ folder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
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