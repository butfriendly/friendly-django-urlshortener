from distutils.core import setup

setup(
    name='friendly-django-urlshortener',
    version='0.0.1',
    author='Daniel Hepper',
    author_email='daniel@butfriendly.com',
    packages=['urlshortener'],
    scripts=[],
    url='http://github.com/butfriendly/friendly-url-shortener',
    license='LICENSE',
    description='A friendly URL shortener app for Django.',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.4",
    ],
)
