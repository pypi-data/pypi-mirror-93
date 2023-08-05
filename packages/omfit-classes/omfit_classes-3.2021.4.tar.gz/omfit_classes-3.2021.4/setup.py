from setuptools import setup
import os
import fnmatch
from pprint import pprint

with open('omfit_classes/version') as f:
    version = f.read().strip()

package_data = ['*']
for root, dir, files in os.walk("omfit_classes"):
    if not len(root[len('omfit_classes'):]):
        continue
    package_data.append(root[len('omfit_classes'):] + os.sep + '*')

setup(
    name='omfit_classes',
    version=version,
    description='class files of One Modeling Framework For Integrated Tasks',
    url='https://omfit.io',
    author='OMFIT developers',
    author_email="meneghini@fusion.gat.com",
    classifiers=['Programming Language :: Python :: 3', 'Operating System :: OS Independent'],
    keywords='integrated modeling plasma framework',
    packages=['omfit_classes', 'omfit_classes.unix_os'],
    package_dir={'omfit_classes': 'omfit_classes', 'omfit_classes.unix_os': 'omfit_classes/unix_os'},
    install_requires=[],
    extras_require={},
    package_data={'omfit_classes': package_data, 'omfit_classes.unix_os': ['unix_os/*']},
)
