from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'blowcurve',
    author = 'origamizyt',
    version = '1.0.0',
    author_email = 'zhaoyitong18@163.com',
    description = 'Simple library for Blowfish / ECC encryption and digital signatures.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/origamizyt/blowcurve',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3',
    install_requires = ['PyCryptodome', 'ecdsa'],
    license='MIT'
)