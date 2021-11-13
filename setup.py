from distutils.core import setup

setup(
    version=1.0,
    name='eudaemon',
    description='Monitor activity and help user to be conscious about it and to take positive action.',
    long_description=open('README.rst', 'rt').read(),
    author='Daniel Souza',
    author_email='me@posix.dev.br',
    url='',
    platforms='Linux',
    license='GPLv3',
    py_modules=['eudaemon'],
)
