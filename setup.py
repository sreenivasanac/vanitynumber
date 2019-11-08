from setuptools import setup, find_packages

exec(open('vanitynumber/version.py').read())

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(name='vanitynumber',
      version=__version__,
      description='Vanity Number Wordification',
      long_description=readme,
      long_description_content_type="text/markdown",
      url='https://github.com/sreenivasanac/vanitynumber',
      keywords = ['Vanity Number', 'Toll-free number', 'Wordification', 'Marketing', 'Phone Number'],
      install_requires=[            # I get to this in a second
          'PyYAML',
          'pygtrie',
          'pytest'
      ],
      download_url = 'https://github.com/sreenivasanac/vanitynumber/archive/v_0.5.tar.gz',
      author='Sreenivasan AC',
      author_email='sreenivasan.nitt@gmail.com',
      license='EULA',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.7',      #Specify which python versions that you want to support
      ],
      zip_safe=False)
