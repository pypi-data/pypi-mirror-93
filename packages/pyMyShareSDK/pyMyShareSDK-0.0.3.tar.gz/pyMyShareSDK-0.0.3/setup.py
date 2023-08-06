from setuptools import setup

base_url = 'https://github.com/LeanderGangso/pyMyShareAPI'

requirements = [
    'requests',
]

requirements_dev = [
    'pytest==6.2.2',
    'check-manifest==0.46',
]

exec(open('mysdk/version.py', 'r').read()) # get __version__ variable

setup(name='pyMyShareSDK',
        version=__version__, # gets version from version.py file
        description='Python SDK for MyShare API ',
        long_description=open('README.md', encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        author='LeanderGangso',
        author_email='Leander.Gangso98@gmail.com',
        url=base_url,
        download_url=f'{base_url}/archive/{__version__}.tar.gz', # download from repo release
        license='MIT',
        keywords='python myshare sdk api tools',
        packages=['mysdk'],
        install_requires=requirements,
        extras_require={
            'dev': requirements_dev
        },
        classifiers=[
            'Development Status :: 1 - Planning', # 3 - Alpha, 4 - Beta, 5 - Production/Stable
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        python_requires='>=3.6'
)

