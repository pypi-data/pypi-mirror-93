from setuptools import setup, find_packages

def read_file(fname):
    try:
        with open(fname) as f:
            return f.read()
    except IOError:
            return 'Under active development ..'


setup(
    name='django-backoffice',
    version='0.0.1.dev0',
    license='BSD 3-Clause',
    description='django backoffice admin theme',
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    author='Nizar DELLELI',
    author_email='nizar.delleli@gmail.com',
    # maintainer='',
    # maintainer_email='',
    keywords='django backoffice theme',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    url='https://github.com/cizario/django-backoffice/',
    download_url='https://github.com/cizario/django-backoffice/',
    project_urls={
        'Tracker': 'https://github.com/cizario/django-backoffice/issues',
        'Source': 'https://github.com/cizario/django-backoffice/',
        # 'Funding': 'https://patreon.com/cizario',
        # 'Say Thanks!': 'http://saythanks.io/to/cizario',
        'Release notes': 'https://github.com/cizario/django-backoffice/releases',
        'Documentation': 'https://django-backoffice.readthedocs.io/en/latest/',
    },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[],
)
