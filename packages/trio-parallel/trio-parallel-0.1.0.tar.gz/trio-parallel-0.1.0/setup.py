from setuptools import setup, find_packages

exec(open("trio_parallel/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="trio-parallel",
    version=__version__,
    description="CPU parallelism for Trio",
    url="https://github.com/richardsheridan/trio-parallel",
    long_description=LONG_DESC,
    author="Richard Sheridan",
    author_email="richard.sheridan@gmail.com",
    license="MIT -or- Apache License 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["trio"],
    keywords=["parallel", "trio", "async", "dispatch"],
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
    ],
)
