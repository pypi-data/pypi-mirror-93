"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='usbwde-mccrab',
    version='2021.01.1',
    author='Gabe Krabbe',
    author_email='krabbe@google.com',
    description='A client class for the USB-WDE1 receiver by ELV.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mccrab/usbwde',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    install_requires=[
        'pyserial',
    ],
    python_requires='>=3.6',
    test_suite='usbwde.tests.usbwde_test',
)
