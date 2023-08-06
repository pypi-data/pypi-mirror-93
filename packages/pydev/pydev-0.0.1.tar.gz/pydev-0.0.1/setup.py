import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = os.getenv('PYDEV_VERSION', '0.0.0')

setuptools.setup(
    name="pydev",
    version=version,
    author="Sagiv Oulu",
    author_email="sagiv.oulu@gmail.com",
    description="A python development environment inside containers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sagbot/pydev",
    license='MIT',
    packages=setuptools.find_packages(),
    scripts=['pydev.py'],
    install_requires=[
        'colorama==0.4.4',
        'pydantic==1.7.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
