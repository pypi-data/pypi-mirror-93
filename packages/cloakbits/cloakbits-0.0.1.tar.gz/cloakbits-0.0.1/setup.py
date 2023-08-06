import setuptools

with open('cloakbits/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="cloakbits",
    version="0.0.1",
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
