from setuptools import setup, find_namespace_packages

__version__ = '1.0.0'

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
   package_data={'dopltech.sdk.bin': ['dopltech/sdk/bin/libsdk_arm.so', 'dopltech/sdk/bin/libsdk_amd64.so', 'dopltech/sdk/bin/libsdk_amd64.dylib', 'dopltech/sdk/bin/libsdk_amd64.dll']},
   include_package_data=True,
)