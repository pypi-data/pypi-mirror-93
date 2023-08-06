from setuptools import setup
from setuptools import find_packages

install_requires = [
    'pymysql==0.9.3',
    'requests==2.24.0',
]

excluded = ('CommonPart.gitignore',)

setup(
    name='CommonPart',
    version='0.0.8',
    author='afcentry',
    author_email='afcentry@163.com',
    url='https://github.com/afcentry',
    description='tools model',
    packages=find_packages(exclude=excluded),
    install_requires=install_requires,
    license = 'BSD License',
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
)
