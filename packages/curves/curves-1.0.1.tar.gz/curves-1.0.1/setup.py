# Copyright(c) 2019 Jake Fowler
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import setuptools
import os

with open('README.md', 'r') as fh:
    long_description = fh.read()

version = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'curves', '__version__.py')) as fp:
    exec(fp.read(), version)

setuptools.setup(
    name='curves',
    version=version['__version__'],
    author='Jake Fowler',
    author_email='jake@cmdty.co.uk',
    description='Tools for building commodity forward, swaps, and futures curves.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cmdty/curves',
    packages=setuptools.find_packages(),
    keywords = 'commodities trading curves oil gas power quantitative finance',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: C#',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python :: 3', # TODO specific Python versions?
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'pythonnet==2.5.1',
        'pandas>=1.0.3'
        ],
    package_data={'curves' : [
                        'lib/*.dll',
                        'lib/*.pdb'
                    ]},
    include_package_data=True
)