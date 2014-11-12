from setuptools import setup, find_packages

version = '0.0.1.dev'

setup(name='tilestache-providers',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires=[
          'modestmaps',
          'boto',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
