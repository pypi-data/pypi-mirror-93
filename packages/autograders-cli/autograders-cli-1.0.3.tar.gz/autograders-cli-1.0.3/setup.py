'''
MIT License

Copyright (c) 2021 Autograders

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import pathlib
import setuptools

# README.md
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    license='MIT',
    name='autograders-cli',
    version='1.0.3',
    author='Andrés Castellanos',
    author_email='andres.cv@galileo.edu',
    description='Autograders Command Line Interface',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/autograders/cli/',
    project_urls={
        'Source': 'https://github.com/autograders/cli/',
        'Documentation': 'https://github.com/Autograders/cli/blob/main/README.md'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'autograder'
    ],
    python_requires='>=3.6',
    install_requires=[
        'certifi >= 2020.12.5',
        'chardet >= 4.0.0',
        'idna >= 2.10',
        'requests >= 2.25.1',
        'tabulate >= 0.8.7',
        'urllib3 >= 1.26.3',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'autograder = autograder.__main__:main'
        ]
    }
)
