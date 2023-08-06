import setuptools
from sliding1d import VERSION_STR

setuptools.setup(
    name='sliding1d',
    version=VERSION_STR,
    description='1D sliding window calculation tools',
    url='https://github.com/gwappa/python-sliding1d',
    author='Keisuke Sehara',
    author_email='keisuke.sehara@gmail.com',
    license='MIT',
    install_requires=[
        'numpy>=1.0',
        'bottleneck>=0.6'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],
    packages=['sliding1d',],
    entry_points={
        # nothing for the time being
    }
)
