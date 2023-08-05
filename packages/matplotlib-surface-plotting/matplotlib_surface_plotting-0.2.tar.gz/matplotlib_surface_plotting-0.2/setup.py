from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='matplotlib_surface_plotting',
      version='0.2',
      packages=find_packages(),
      install_requires=['nibabel',
                        'matplotlib>=3.3.2'],
      package_dir={'matplotlib_surface_plotting':'matplotlib_surface_plotting'},
      url="https://github.com/kwagstyl/matplotlib_surface_plotting"
     )
