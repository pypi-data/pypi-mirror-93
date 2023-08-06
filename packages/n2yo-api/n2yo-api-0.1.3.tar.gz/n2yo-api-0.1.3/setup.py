import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='n2yo-api',
    version='0.1.3',
    author='F. A. Corazza',
    author_email='federico.corazza@live.it',
    description='Python wrapper for the N2YO API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/facorazza/n2yo-api',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
