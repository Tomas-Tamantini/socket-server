from setuptools import setup, find_packages

req_file = 'requirements.txt'
with open(req_file) as f:
    requirements = f.read().splitlines()

setup(
    name='socket-server',
    version='0.1',
    description='A (hopefully) simple socket server',
    author='Tomas Tamantini',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True
)
