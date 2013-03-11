from distutils.core import setup

setup(
    name='Demoize',
    version='0.1.0',
    author='Jonathan Lipps',
    author_email='jlipps@gmail.com',
    packages=['demoize'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/Demoize/',
    license='LICENSE.txt',
    description='A webserver that shows your code as it is executed',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask >= 0.9",
    ],
)
