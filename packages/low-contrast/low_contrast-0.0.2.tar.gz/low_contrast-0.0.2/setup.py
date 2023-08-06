from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'low-contrast'
LONG_DESCRIPTION = 'Package to detect images with lower contrast'

# Setting up
setup(
    name="low_contrast",
    version=VERSION,
    author="Amol Patil",
    author_email="<amolkumar.work@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)