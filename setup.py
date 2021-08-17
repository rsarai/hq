# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='hq',  # Required
    version='0.0.1',  # Required
    description='A package to manage my personal data.',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/rsarai/hq',  # Optional
    author='Rebeca Sarai',  # Optional
    author_email='rebecasaraiaguiar@gmail.com',  # Optional
    keywords='quantifiedself, hq',  # Optional
    packages=find_packages(include=['hq']),  # Required
    python_requires='>=3.6, <4',
    install_requires=['orger', 'pytz'],  # Optional
    entry_points={
        'console_scripts': [
            'mount_memex=hq.routines.importer:mount_memex',
            'update_memex=hq.routines.importer:update_memex',
            'reset=hq.routines.importer:reset',
            'inc=hq.routines.incremental_notes:append',
            'scan=hq.routines.scan_repos:run',
        ],
    },
)
