from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='skidings',
    version='0.0.9',
    description='Simple module for new comers to networking and requests and mysql',
    long_description=open('README.txt').read(),
    url='https://github.com/AeronPY/SkidingsPY-module',
    author='AeronPY',
    author_email='aeron1337@protonmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='skidings',
    packages=find_packages(),
    install_requires=['mysql-connector', 'datetime', 'dhooks']
)