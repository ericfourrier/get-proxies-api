from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='gpapi',
      version= "0.1",
      description='A quick python wrapper of the theproxisright api',
      long_description=readme(),
      author='Eric Fourrier',
      author_email='ericfourrier0@gmail.com',
      license = 'MIT',
      #url=
      packages=['gpapi'],
      keywords=['proxies','get', 'api'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests>=2.0']
)