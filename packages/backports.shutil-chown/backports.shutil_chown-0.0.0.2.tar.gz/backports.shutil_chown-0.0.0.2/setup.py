from setuptools import setup

setup(
    name='backports.shutil_chown',
    description='backports shutil chown (mainly for Python2)',
    long_description=open("README.md").read(),
    version='0.0.0.2',
    url='https://github.com/cielavenir/backports.shutil_chown',
    license='0BSD',
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    packages=['backports'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
