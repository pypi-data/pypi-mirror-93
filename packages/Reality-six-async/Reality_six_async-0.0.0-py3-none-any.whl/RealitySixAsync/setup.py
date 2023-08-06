
des=open("RealitySixAsync/README.md","r",encoding="utf-8")
long=des.read()
import setuptools
setuptools.setup(
    name="Reality-six-async", 
    version="0.0.0", 
    author="pkg_uploaders", 
    author_email="example@example.com", 
    description="A simple package that tells you reality. Async. Unsupported", 
    long_description=long,
    long_description_content_type="text/markdown",install_requires=["psutil>=5.8.0"],
    url="https://github.com/Hillo232/Reality/tree/async", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)