from setuptools import setup, find_packages
import sys

version = '1.0.3'
long_description = ""
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()
# setup
setup(
    name="roi-device",
    version=version,
    description="roi aliyun iot device",
    author="labelnet",
    author_email="labelnet@smartahc.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/roi-iot-device/",
    keywords=['roi'],
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'aliyun-iot-linkkit==1.2.2',
        'pycryptodome==3.7.2'
    ],
    python_requires='>=3.5'
)
