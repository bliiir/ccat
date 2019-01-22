from setuptools import setup, find_packages

setup(
    name='ccat',
    version='0.1',
    description='Crypto Currency Auto Trader',
    url='https://github.com/bliiir/ccat',
    author='bliiir',
    #author_email='hemmeligholte@gmail.com',
    license='MIT',
    packages=find_packages(),
    # install_requires=[
    #       'ccxt',
    #       'pandas',
    #       'numpy',
    #       'psycopg2-binary',
    #       'SQLAlchemy'
    # ],
    zip_safe=False
    )
