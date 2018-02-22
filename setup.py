from __future__ import division, print_function, absolute_import
from setuptools import setup

# long description
def readme(fname):
    with open(fname) as f:
        text = f.read()
    return text


dependencies = [
    'click>=4.0',
    'numpy>=1.11',
    'pandas>=0.18',
    'setuptools>=33.0',
    ]

setup(
    name='labchartio',
    version='0.1',
    description='Binary decoder for MRI field dosimeter LabChart binary files.',
    long_description=readme('README.rst'),
    author='Jamie Roberts',
    author_email='jrobertsink@gmail.com',
    url='https://github.com/jamie-roberts/labchartio',
    download_url='',
    license='MIT',
    install_requires=dependencies,
    py_modules=['labchartio'],
    entry_points='''
        [console_scripts]
        labchartio=labchartio:main
    ''',
    zip_safe=False,
)