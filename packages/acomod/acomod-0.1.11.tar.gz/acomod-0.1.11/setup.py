from setuptools import setup
import os

import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)
    
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

required_packages=read('requirements.txt').split()

setup(name='acomod',
      version='0.1.11',
      description='Acoustic Oscillations Viewer',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      author='Bartosz Lew',
      author_email='bartosz.lew@protonmail.com',
      url='https://github.com/bslew/acomod',
      install_requires=required_packages,
      package_dir = {'': 'src'},
      packages = ['acomod',
                  ],
      entry_points={ 'gui_scripts': [ 'acoustic_mode_viewer = acomod.sonidist:main',
               ],
                    },
      package_data={'acomod': ['*.ui','resources.qrc'
                               ]},
#       eager_resources={'acomod': ['data/*.wav','data/*.WAV',
#                                ]},
    data_files=[('data', ['src/acomod/data/cow.wav',
                             ])],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
        ],
     )
