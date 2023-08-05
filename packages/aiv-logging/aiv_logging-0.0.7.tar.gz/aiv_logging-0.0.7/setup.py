from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Aiv_logging make by AI Academy Viet Nam'
LONG_DESCRIPTION = 'Logging packages are used in common within AI Academy Viet Nam'

# Setting up
setup(
    name="aiv_logging",
    version=VERSION,
    author="Toan Silver",
    author_email="ngoctoan1105@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["colorlog"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'aiv', 'logging'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)