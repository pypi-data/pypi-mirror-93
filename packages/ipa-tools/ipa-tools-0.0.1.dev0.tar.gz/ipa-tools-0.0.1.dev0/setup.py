from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='ipa-tools',
      version='0.0.1',
      description=u"iPA client",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Roberto Reale",
      author_email='roberto@reale.me',
      url='https://github.com/reale/ipa-tools',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest', 'jsonschema'],
      },
      entry_points="""
#      [console_scripts]
#      ipa-tools=ipa-tools.scripts.cli:cli
#      """
      )
