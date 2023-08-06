#!/usr/bin/env python3
import setuptools


if __name__ == '__main__':
    setuptools.setup(
        version='1.2.1',
        setup_requires=[
            'setuptools'
        ],
        install_requires=[
            'BlueWhale3>=3.23.0',
            'BlueWhale3-bioinformatics>=4.0.0',
            'fastdtw==0.3.2',
            'pandas>=0.23,<1.1',
            'loompy>=2.0.10',
            'xlrd~=1.2.0',
            'anndata>=0.6.21',
            'numpy',
            'scikit-learn',
        ],
        extras_require={
            'doc': ['sphinx', 'recommonmark'],
            'package': ['twine', 'wheel'],
            'test': [
                'pytest~=5.1.0',
                'pytest-cov~=2.7.1',
                'coverage~=4.5.4',
                'codecov~=2.0.15'
            ],
        },
    )
