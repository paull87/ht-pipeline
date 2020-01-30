from setuptools import setup, find_packages

setup(
    name='htpipeline',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy',
        'awscli',
        'boto3',
        'jupyter',
        'numpy',
        'openpyxl',
        'pandas',
        'numpy',
        'pyspark',
        'pytest',
        'pywinrm',
        'requests',
        'pyodbc',
    ]
)
