from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='menhir.simple.comments',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['menhir', 'menhir.simple'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'dolmen.forms.base',
          'grokcore.annotation',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
