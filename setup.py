import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bls_datasets',
    version='0.0.8',
    description='Python library for retrieving BLS datasets',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/mbkupfer/bls-datasets',
    author='Maxim Kupfer',
    author_email='mbkupfer@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering',
    ],
    keywods='bls oes qcew',
    packages=['bls_datasets'],
    install_requires=[
        'pandas>=0.23.4',
        'xlrd>=1.1.0',
        'requests>=2.19.1',
    ],
)
