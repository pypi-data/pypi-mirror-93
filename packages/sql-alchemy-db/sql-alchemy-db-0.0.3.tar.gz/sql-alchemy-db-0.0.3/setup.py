from setuptools import setup, find_packages

setup(
    name='sql-alchemy-db',
    version='0.0.3',
    description='SQLAlchemy utility library',
    url='https://github.com/alenlukic/sql-alchemy-db',
    author='Alen Lukic',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['SQLAlchemy==1.3.10'],
    packages=find_packages(),
    download_url='https://github.com/alenlukic/sql-alchemy-db/archive/0.0.3.zip',
    python_requires='>=3, <4'
)
