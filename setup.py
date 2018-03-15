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
        "pymysql",
        "beanstalkc",
        "coloredlogs"
    ],
    entry_points={
        'console_scripts': [
            'pear_web = pear.web.app:main',
            'job_queue = pear.jobs.manager:main'
        ]
    }
)
