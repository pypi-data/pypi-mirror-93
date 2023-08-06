from setuptools import setup,find_packages
from os import path as os_path

#from testrelease import _version
__version__ = "3.1"

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='testrelease',
    python_requires='>=3.6',
    version=__version__,#_version.__version__,
    description="testrelease",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="testrelease",
    author_email='',
    url='',
    #packages=['testrelease'],
    packages=find_packages(),
    #packages = ['.','testrelease'],
    #package_data={'testrelease':['*']},
    zip_safe=False,
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    license="BSD 3-Clause",
    keywords=['testrelease', 'bim', 'testrelease framework'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
