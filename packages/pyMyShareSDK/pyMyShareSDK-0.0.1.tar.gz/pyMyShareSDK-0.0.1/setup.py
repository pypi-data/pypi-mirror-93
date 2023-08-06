from setuptools import setup
from io import open
import re

base_url = 'https://github.com/LeanderGangso/pyMyShareAPI'

requirements = ['requests']

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

with open('mysdk/version.py', 'r', encoding='utf-8') as f:
    version = re.search(r"^__version__\s*=\s*'(.*)'.*$", f.read(), flags=re.MULTILINE).group(1)

setup(name='pyMyShareSDK',
        version=version, # gets version from version.py file
        description='Easy MyShare SDK for Python',
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        author='LeanderGangso',
        author_email='Leander.Gangso98@gmail.com',
        url=base_url,
        download_url=f'{base_url}/archive/v{version}.tar.gz', # download from repo release
        license='MIT',
        keywords='python myshare sdk api tools',
        packages=['mysdk'],
        install_requires=requirements,
        extras_require={
            'json': 'ujson',
            'dev': [
                'twine',
                'pytest',
                'check-manifest',
                'setuptools',
                'wheel',
            ]
        },
        classifiers=[
            'Development Status :: 1 - Planning', # 3 - Alpha, 4 - Beta, 5 - Production/Stable
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        python_requires='>=3.6'
)

