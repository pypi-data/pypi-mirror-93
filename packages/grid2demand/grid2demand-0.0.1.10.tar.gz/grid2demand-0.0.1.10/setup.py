# python setup.py sdist
# twine upload dist/*0.0.1.2*

import setuptools
import io
import os


setuptools.setup(
    name='grid2demand',
    version='0.0.1.10',
    author='Anjun Li, Xuesong (Simon) Zhou, Entai Wang, Taehooie Kim',
    author_email='li.anjun@foxmail.com, xzhou74@asu.edu, entaiwang@bjtu.edu.cn',
    url='https://github.com/asu-trans-ai-lab/grid2demand/',
    description='A quick trip generation and distribution tool based on the four-step travel mode',
    long_description=open('README.md', encoding='utf-8').read(),   
    long_description_content_type='text/markdown',
    license='MIT Licence',
    packages=['grid2demand'],
    python_requires=">=3.6.0",
    install_requires=['pandas >= 0.24.0','shapely >= 1.6','protobuf >= 3.14.0','pyproj','numpy'],
    classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 3']
)
