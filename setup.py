from setuptools import find_packages, setup

setup(
    name='pear',
    version='0.0.1',
    license='PRIVATE',
    author='',
    author_email='',
    description=u'',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        "requests",
        "flask",
        "sqlalchemy",
        "flask_sqlalchemy",
    ],
    entry_points={
        'console_scripts': [

        ],
    }
)
