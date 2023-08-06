from setuptools import find_packages, setup

setup(
    name='semilimes',
    packages=find_packages(include=['semilimes']),
    version='0.1.1',
    description='Python lib for semilimes ws',
    author='Flavio Ansovini',
    license='gpl-3.0',
    install_requires=['websocket-client','numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)