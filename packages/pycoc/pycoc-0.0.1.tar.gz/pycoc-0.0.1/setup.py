from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pycoc',
    version='0.0.1',
    packages=['pycoc'],
    url='',
    license='Artistic-2.0',
    author='Frank T. Bergmann',
    author_email='frank.bergmann@bioquant.uni-heidelberg.de',
    description='PyCoC - an easy to use COPASI API for python',
    platforms=['Windows', 'Linux', 'MacOS'],
    classifiers=[
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Artistic License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='copasi sbml systems biology',
)
