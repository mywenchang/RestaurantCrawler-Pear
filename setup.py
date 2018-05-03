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
        "PyYAML",
        "gunicorn",
        'mock',
        'pytest',
        'coloredlogs',
        'selenium',
        'geohash2',
        'jieba',
        'wordcloud',
        'Pillow',
        'numpy',
        'matplotlib',
        'beautifulsoup4',
        'html5lib'
    ],
    entry_points={
        'console_scripts': [
            'job_queue = pear.jobs.manager:main',
            'web = pear.web.app:main'
        ]
    }
)
