import os
from setuptools import setup, find_packages


VERSION = '0.0.2'
INSTALL_REQUIRES = [
    "flax>=0.3.0"
]
PKG_NAME='baxa'

cwd = os.path.dirname(os.path.abspath(__file__))
def write_version_file():
    version_path = os.path.join(cwd, PKG_NAME, "version.py")
    with open(version_path, "w") as f:
        f.write("__version__ = '{}'\n".format(VERSION))
write_version_file()


setup(
    name=PKG_NAME,
    version=VERSION,
    url='https://github.com/prabhuomkar/baxa',
    license='Apache 2.0',
    author='Omkar Prabhu',
    author_email='prabhuomkar@pm.me',
    description='Models and examples built with JAX',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=('tests', 'docs', 'scripts')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)