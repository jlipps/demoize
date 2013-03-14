from distutils.core import setup

setup(
    name='Demoize',
    version='0.1.6',
    author='Jonathan Lipps',
    author_email='jlipps@gmail.com',
    packages=['demoize', 'demoize.web'],
    package_data={'demoize.web': ['static/*',
                                  'templates/*']},
    #data_files=[('web/static', ['demoize/web/static/*']),
                #('web/templates', ['demoize/web/templates/*'])],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/Demoize/',
    license='LICENSE.txt',
    description='A webserver that shows your code as it is executed',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask >= 0.9",
        "pygments >= 1.6",
        "selenium >= 2.31",
    ],
)
