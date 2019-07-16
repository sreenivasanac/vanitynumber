from setuptools import setup

exec(open('vanitynumber/version.py').read())

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(name='vanitynumber',
      version=__version__,
      description='Vanity Number Wordification',
      long_description=readme,
      long_description_content_type="text/markdown",
      url='https://github.com/sreenivasanac/vanitynumber',
      author='Sreenivasan AC',
      author_email='sreenivasan.nitt@gmail.com',
      license='EULA',
      packages=['vanitynumber'],
      zip_safe=False)
