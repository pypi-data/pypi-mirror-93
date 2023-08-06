from setuptools import setup, find_namespace_packages

__version__ = '1.0.1'

setup(
   name='dopltech-sdk',
   version=__version__,
   description='Dopl Technologies SDK',
   author='Ryan James',
   author_email='ryan@dopltechnologies.com',
   url='https://github.com/dopl-technologies/sdk-python',
   keywords=['dopl', 'technologies', 'telerobotics', 'sdk', 'electrophysiology', 'medicine'],
   packages=find_namespace_packages(include=['dopltech.*']),
   install_requires=['dopltech-api-protos', 'grpcio', 'grpcio-tools'],
)