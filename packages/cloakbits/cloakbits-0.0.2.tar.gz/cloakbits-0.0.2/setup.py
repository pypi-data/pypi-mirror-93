import setuptools

pkg_version = None

with open('cloakbits/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            pkg_version = line.strip().split('=')[1].strip(' \'"')
            break

assert pkg_version

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="cloakbits",
    version=pkg_version,
    author="Cloakbits",
    author_email="dev@cloakbits.co",
    description="A utility for managing Cloakbits stealth sessions.",
    url="https://github.com/cloakbits/cloakbits-python",
    packages=setuptools.find_packages(include=['cloakbits', 'cloakbits.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    extras_require={'test': ['pytest', 'pytest-watch', 'tox']},
    install_requires=install_requires,
)
