import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
      name='py-repo-root',
      version='0.4.0',
      license='MIT',
      description='Python utility for cleaner handling of paths',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/microsoft/project-root',
      packages=setuptools.find_packages(),
      python_requires=">=3.7.0",
      include_package_data=True,
      author='Pashmina Cameron, Henry Jackson Flux',
      author_email = "pashabhi@yahoo.com",
      install_requires=[
          'pathlib', 'typing-extensions'
      ],
      zip_safe=False)
