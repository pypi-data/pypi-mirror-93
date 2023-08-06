
from distutils.core import setup
from setuptools import find_packages
 
setup(name = 'bindows',     # 包名
      version = '0.1.0',  # 版本号
      description = 'Copy from Windows',
      long_description = 'Copy from Windows',
      author = 'Blueice -- Lanbinshijie',
      author_email = 'huoziye123@163.com',
      url = 'https://www.codesra.cn/',
      license = '',
      install_requires = [],
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
      ],
      keywords = 'Bindows',
      packages = find_packages('src'),  # 必填
      package_dir = {'':'src'},         # 必填
      include_package_data = True,
)