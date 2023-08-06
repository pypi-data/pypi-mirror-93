'''
Copyright (C) Optumi Inc - All rights reserved.

You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
'''

import os
from glob import glob
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

version_ns = {}
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jupyterlab-optumi', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name='jupyterlab-optumi',
    version=version_ns['__version__'],
    url='https://www.optumi.com',
    description='Offload Jupyter notebooks from your laptop into the cloud',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Optumi Inc Authors',
    author_email='cs@optumi.com',
    packages=find_packages(),
    install_requires=[
        'jupyterlab>=2,<3',
        'notebook>=6.0.0',
        'cryptography>=3.0',
        'tornado>=6.0'
    ],
    include_package_data=True,
    data_files=[
    	('etc/jupyter/jupyter_notebook_config.d',['jupyterlab-optumi.json']),
    	('share/jupyter/lab/extensions', glob('jupyterlab-optumi*.tgz'))
    ],
    classifiers=[
    	'License :: Other/Proprietary License',
    	'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6'
)

if __name__ == '__main__':
    setup(**setup_args)
