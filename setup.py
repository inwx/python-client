import setuptools

version = '3.1.0'

with open("requirements.txt", "r") as fh:
    install_requires = fh.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='inwx-domrobot',
    version=version,
    author='INWX Developer',
    author_email='developer@inwx.de',
    description='INWX API Python Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/inwx/python-client',
    download_url='https://github.com/inwx/python-client/archive/v' + version + '.tar.gz',
    packages=setuptools.find_packages(),
    keywords=['INWX', 'API', 'PYTHON', 'CLIENT', 'DOMROBOT'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
