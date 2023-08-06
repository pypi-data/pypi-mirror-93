from setuptools import setup, find_packages

setup(
    name='kkpy',
    version='0.2.0',
#    packages=find_packages(exclude=['tests*']),
    packages=['kkpy'],
    package_dir={'kkpy': 'kkpy'},
    package_data={'kkpy': ['SHP/*']},
    license='MIT',
    description='My python package',
#    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    long_description='README.md',
    install_requires=[
        'numpy',
        'Cartopy',
        'wradlib',
        'arm_pyart',
        'matplotlib',
        'haversine',
        'scipy',
        'dask',
        'pandas',
        'netCDF4',
        'geopandas',
        'descartes',
        'xarray',
        'bottleneck',
        'scikit-image'],
    url='https://github.com/Kwonil-Kim/kkpy',
    author='Kwonil Kim',
    author_email='kwonil.kim.0@gmail.com'
)
