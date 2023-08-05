from setuptools import setup, find_namespace_packages

__version__ = "0.0.1"

setup(
   name='dopltech-api-protos',
   version=__version__,
   description='Dopl Technologies API protos',
   author='Ryan James',
   author_email='ryan@dopltechnologies.com',
   packages=find_namespace_packages(include=['dopltech.*']),
   install_requires=['grpcio', 'grpcio-tools'],
)