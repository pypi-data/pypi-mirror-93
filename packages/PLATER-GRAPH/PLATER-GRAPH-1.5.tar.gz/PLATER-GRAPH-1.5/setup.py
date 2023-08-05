#from distutils.core import setup
from setuptools import setup
import os
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = f"See the Homepage for a better formatted version.\n {long_description}"
setup(
    name = 'PLATER-GRAPH',
    packages = ['PLATER',
    'PLATER/services',
    'PLATER/tests',
    'PLATER/services/util',
    'PLATER/services/util/drivers'],
    data_files= [('',['PLATER/services/plater.conf', 'PLATER/logs/plater.log'])],
    version = '1.5',
    description = 'TranslatorAPI Interface for graph databases.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = '',
    author_email = 'yaphetkg@renci.org',
    install_requires = [
      'coverage',
      'pyaml==20.3.1',
      'pytest==5.4.1',
      'pytest-asyncio==0.14.0',
      'starlette==0.13.6',
      'uvicorn==0.11.7',
      'httpx',
      'redis'
    ],
    include_package_data=True,
    entry_points = {
    },
    dependencies= [
    'git+git://github.com/patrickkwang/biolink-model-toolkit@master#egg=bmt',
    'git+https://github.com/ranking-agent/reasoner.git',
    'git+https://github.com/TranslatorSRI/reasoner-pydantic@v1.0#egg=reasoner-pydantic',
    'git+https://github.com/patrickkwang/fastapi#egg=fastapi',
    'git+https://github.com/redislabs/redisgraph-py.git'
    ],
    url = 'http://github.com/YaphetKG/plater.git',
    download_url = 'http://github.com/yaphetkg/plater/archive/GRAPH-PLATER-1.5.tar.gz',
    keywords = [ 'knowledge', 'network', 'graph', 'biomedical' ],
    classifiers = [ ],
)
