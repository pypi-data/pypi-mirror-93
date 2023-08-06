from distutils.core import setup
import setuptools

setup(
    name='mesa-solutions-utils',
    packages=['MesaSoapManager'],
    version='1.0.0',
    license='MIT',
    description='Manages SOAP connection for NAV',
    author='Mesa Natural Gas Solutions, LLC',
    author_email='support@mesangs.com',
    url='https://dev.azure.com/mesa-ngs/_git/nav-soap-manager',
    download_url='https://dev.azure.com/mesa-ngs/_git/nav-soap-manager',
    keywords=['Microsoft Dynamics NAV', 'SOAP'],
    install_requires=[
        'zeep',
    ]
)
