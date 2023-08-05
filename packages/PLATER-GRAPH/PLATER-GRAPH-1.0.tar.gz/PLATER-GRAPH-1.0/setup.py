#from distutils.core import setup
from setuptools import setup, find_packages
import os
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = f"See the Homepage for a better formatted version.\n {long_description}"
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]
install_reqs = parse_requirements("PLATER/requirements.txt")
requirements = [str(r) for r in install_reqs]
setup(
    name = 'PLATER-GRAPH',
    packages = ['PLATER',
    'PLATER/services',
    'PLATER/tests',
    'PLATER/services/util',
    'PLATER/services/util/drivers'],
    package_data= {'PLATER/services/': ['plater.conf' ]},
    version = '1.0',
    description = 'TranslatorAPI Interface for graph databases.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = '',
    author_email = 'yaphetkg@renci.org',
    install_requires = 'requirements.txt',
    include_package_data=True,
    entry_points = {
    },
    url = 'http://github.com/YaphetKG/plater.git',
    download_url = 'http://github.com/yaphetkg/plater/archive/GRAPH-PLATER-1.0.tar.gz',
    keywords = [ 'knowledge', 'network', 'graph', 'biomedical' ],
    classifiers = [ ],
)
