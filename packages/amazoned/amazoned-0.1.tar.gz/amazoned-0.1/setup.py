import setuptools

classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]

setuptools.setup(
    name='amazoned',
    version='0.1',
    author='youngtrep',
    author_email='youngtrep.business@gmail.com',
    description='Amazon link to affiliate link',
    long_description=open('README.txt').read(),
    url='https://github.com/YoungTrep/Python-Amazoned',
    packages=setuptools.find_packages(),
    classifiers=classifiers,
    python_requires='>=3.6'
)