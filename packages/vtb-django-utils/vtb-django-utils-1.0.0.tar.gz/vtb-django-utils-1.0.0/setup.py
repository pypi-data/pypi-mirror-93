from setuptools import setup, find_packages

"""
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
"""

REQUIRED = [
]

setup(
    name='vtb-django-utils',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.region.vtb.ru/projects/PUOS/repos/vtb-django-utils',
    license='',
    author='VTB',
    author_email='',
    description='django utils for VTB projects',
    install_requires=REQUIRED,
    extras_require={
        'test': [
            'pytest',
            'pytest-env',
            'pylint',
            'pytest-asyncio'
        ]
    }
)
